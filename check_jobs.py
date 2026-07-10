"""
job-tracker  –  check_jobs.py
Daily scraper: finds new job postings across companies and emails a digest.

Improvements in this version
─────────────────────────────
1.  Two-pass scraping  – Pass 1: fast requests+BS4. If output looks like
    garbage (too few real job titles, too many generic strings), Pass 2
    fires Playwright to render the JS and try again.
2.  Network-intercept fallback  – for sites that load jobs via a JSON API
    call in the browser, Playwright intercepts the XHR/fetch response and
    pulls structured job data directly.
3.  Deduplication  – same company + same normalised title seen on multiple
    boards is collapsed to one entry in the digest.
4.  Seniority filter  – intern / junior / technician / associate titles
    suppressed from digest (score floored at 0, hidden unless score > 0
    from domain keywords).
5.  Garbage detection  – heuristic that flags a scrape result as noise
    before it ever reaches the email.
6.  Retry logic  – requests retried with exponential backoff via Session.
7.  Scrape summary  – email header shows X/Y companies scraped OK.
8.  Failure notification  – separate step in workflow emails on crash.
9.  seen_jobs.json pruning  – entries older than 90 days removed.
10. latest_digest.html committed alongside latest_digest.txt.
11. HTML email sorted by relevance score, grouped by company.
12. Playwright uses domcontentloaded (faster, avoids networkidle timeouts).
13. Zero-score jobs stored with scored=False flag; re-evaluated each run.
14. Minimum link threshold – Pass 1 with < 3 links escalates to Playwright.
15. LinkedIn URLs warn clearly rather than silently skipping.
16. Notion pages detected and warned (JS-rendered, cannot be scraped).
17. Weekly search sweep – discovers new companies not in YAML.
18. URL canonicalization – tracking params stripped before hashing, prevents
    duplicate seen_jobs entries for the same posting with different referral params.
19. Title canonicalization – location suffixes, remote tags, pipe junk stripped
    before scoring, producing cleaner digest titles.
20. Three-bucket scoring – seniority / function / domain scored and capped
    independently, preventing URL keyword inflation.
21. JSON-LD title extraction – structured data checked before <title> tag,
    giving more accurate job titles from ATS pages.
22. Concurrent title fetching – fetch_title calls run in a thread pool
    (20 workers) instead of sequentially, cutting runtime by ~90% on large
    company lists.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import smtplib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parsedate_to_datetime
from urllib.parse import (
    parse_qsl, urlencode, urljoin, urldefrag, urlparse, urlunparse,
)

import requests
import yaml
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger("job-tracker")

# constants
SEEN_FILE = "seen_jobs.json"
SEARCH_CACHE_FILE = "search_cache.json"
HEALTH_FILE = "company_health.json"

# Board-health attention thresholds (units: consecutive daily runs)
FAIL_ATTENTION_STREAK = 3     # scraper errored this many runs in a row
EMPTY_ATTENTION_STREAK = 30   # produced items before, now zero for this long
NEW_BOARD_GRACE_RUNS = 7      # never produced anything within this many runs
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Minimum number of job links Pass 1 must find before we trust the result.
# Below this threshold we escalate to Playwright even if titles look clean.
MIN_LINK_THRESHOLD = 3

# URL canonicalization: tracking params to strip before hashing
TRACKING_PARAM_PREFIXES = ("utm_", "gh_", "mc_", "mkt_", "ref", "src", "trk", "tracking")
TRACKING_PARAM_EXACT = {
    "ashby_jid", "jobsource", "lever-source", "lever-via", "source",
    "linkedin", "linkedin_apply", "li_fat_id", "li_source",
    "fbclid", "gclid", "gad_source", "mc_cid", "mc_eid",
}

# Location/format words stripped from job titles
REMOTE_WORDS = {
    "remote", "hybrid", "onsite", "united states", "usa", "us", "u.s.",
    "u.s.a.", "north america", "europe", "uk", "united kingdom", "canada",
    "global", "multiple locations", "various locations",
    "remote us", "remote usa", "remote within the us", "remote in the us",
    "m/f/d", "f/m/d",
}

# ─────────────────────────────────────────────────────────────────────────────
# RELEVANCE KEYWORDS  –  three independent scored buckets
# ─────────────────────────────────────────────────────────────────────────────
#
# Each bucket is capped independently before summing, so a URL packed with
# domain keywords can't inflate seniority/function scores.
#
#   seniority cap  = 5
#   function  cap  = 8
#   domain    cap  = 10
#
# Scoring philosophy within each bucket:
#   5 = near-perfect signal
#   4 = strong match
#   3 = good signal
#   2 = weak/supporting signal
# ─────────────────────────────────────────────────────────────────────────────

SENIORITY_KEYWORDS: list[tuple[str, int]] = [
    ("vp", 3),
    ("vice president", 3),
    ("head of", 3),
    ("director", 3),
    ("senior manager", 2),
    ("principal", 2),
    ("chief", 2),
    # Exact seniority+function combos that are unambiguous
    ("commercial director", 5),
    ("director of commercial", 5),
    ("head of commercial", 5),
    ("vp commercial", 5),
    ("vp of commercial", 5),
    ("chief commercial officer", 5),
    ("cco", 4),
]

FUNCTION_KEYWORDS: list[tuple[str, int]] = [
    ("business development", 4),
    ("strategic partnerships", 5),
    ("revenue partnerships", 5),
    ("data partnerships", 5),
    ("partnerships", 4),
    ("commercialization", 4),
    ("commercial strategy", 4),
    ("commercial", 3),
    ("go-to-market", 4),
    ("gtm", 4),
    ("sales", 3),
    ("enterprise sales", 4),
    ("account executive", 3),
    ("enterprise account executive", 4),
    ("account director", 3),
    ("account manager", 2),
    ("client partner", 3),
    ("strategic accounts", 3),
    ("industry lead", 3),
    ("market development", 4),
    ("growth", 2),
    ("customer success", 2),
    ("solutions engineer", 2),
    ("solutions consultant", 2),
    ("presales", 2),
    ("pre-sales", 2),
    ("strategy", 3),
    ("alliances", 3),
    ("ecosystem", 2),
    ("channel", 2),
    ("product marketing", 3),
    ("product manager", 2),
    ("portfolio strategy", 3),
    ("licensing", 5),
    ("data licensing", 5),
    ("commercial licensing", 5),
    ("data commercialization", 4),
    ("earned revenue", 4),
    ("revenue", 2),
]

DOMAIN_KEYWORDS: list[tuple[str, int]] = [
    # Earth observation / satellite
    ("earth observation", 5),
    ("satellite imagery", 5),
    ("satellite data", 5),
    ("remote sensing", 5),
    ("sar", 5),
    ("synthetic aperture radar", 5),
    ("optical imagery", 4),
    ("multispectral", 4),
    ("hyperspectral", 4),
    ("lidar", 3),
    ("radar", 3),
    ("space data", 3),
    ("aerial imagery", 3),
    ("geospatial", 4),
    ("gis", 3),
    ("constellation", 3),
    ("tasking", 3),
    ("multi-mission", 4),
    ("data access", 3),
    # Maritime / vessel
    ("maritime", 5),
    ("vessel", 4),
    ("shipping", 3),
    ("ais", 5),
    ("ais data", 5),
    ("fishing", 4),
    ("iuu", 5),
    ("illegal fishing", 5),
    ("ocean", 3),
    ("marine", 3),
    ("port", 2),
    ("dark vessel", 4),
    ("vessel monitoring", 5),
    ("dark shipping", 4),
    # Environment / climate
    ("environmental monitoring", 5),
    ("climate", 3),
    ("carbon", 3),
    ("emissions", 3),
    ("sustainability", 2),
    ("esg", 3),
    ("deforestation", 4),
    ("forest monitoring", 5),
    ("biodiversity", 3),
    ("nature-based", 3),
    ("oil spill", 5),
    ("methane", 4),
    ("ghg", 3),
    ("greenhouse gas", 3),
    ("flood", 3),
    ("wildfire", 3),
    ("forestry", 3),
    # Risk / finance
    ("supply chain", 4),
    ("risk", 3),
    ("risk intelligence", 4),
    ("insurance", 3),
    ("reinsurance", 3),
    ("sanctions", 3),
    ("compliance", 2),
    ("trade intelligence", 4),
    ("commodity", 3),
    ("due diligence", 3),
    # Government / defence
    ("government", 2),
    ("defense", 2),
    ("intelligence", 2),
    ("national security", 3),
    # Agriculture
    ("agriculture", 3),
    ("agri", 2),
    ("crop", 2),
    ("food security", 3),
    ("rf", 4),
    ("radio frequency", 4),
    # Data / platform
    ("data products", 3),
    ("data platform", 2),
    ("api", 2),
    ("analytics", 2),
]

# Titles containing these tokens are junior/support roles –
# suppressed unless they pick up enough domain-keyword score (>= 4)
JUNIOR_TOKENS = re.compile(
    r"\b(intern|internship|junior|jr\.?|technician|technologist|apprentice|"
    r"trainee|associate(?!\s+director)|coordinator|specialist)\b",
    re.IGNORECASE,
)

# Patterns indicating a title is navigation noise rather than a real job
GARBAGE_TITLE_PATTERNS = re.compile(
    r"^(jobs|careers|job openings|career opportunities|open positions|"
    r"current vacancies|work with us|join us|our team|about us|sign in|login|"
    r"apply|apply now|submit application|candidate pool|bamboohr|teamtailor|"
    r"rippling|dover|jazzhr|page_title|\(untitled\)|jobs archive|job listings|"
    r"candidatura|candidature|bewerbung|show more|load more|next page|previous page|"
    r"footer\.|social_link|nav_|menu_)$",
    re.IGNORECASE,
)

def _compile_word_pattern(term: str) -> re.Pattern[str]:
    esc = re.escape(term.lower())
    if re.fullmatch(r"[a-z0-9 ]+", term.lower()):
        return re.compile(rf"(?<![a-z0-9]){esc}(?![a-z0-9])", re.IGNORECASE)
    return re.compile(esc, re.IGNORECASE)


SENIORITY_PATTERNS = [(_compile_word_pattern(k), v) for k, v in SENIORITY_KEYWORDS]
FUNCTION_PATTERNS  = [(_compile_word_pattern(k), v) for k, v in FUNCTION_KEYWORDS]
DOMAIN_PATTERNS    = [(_compile_word_pattern(k), v) for k, v in DOMAIN_KEYWORDS]


def _bucket_score(text: str, patterns: list[tuple[re.Pattern[str], int]], cap: int) -> int:
    score = 0
    for pattern, weight in patterns:
        if pattern.search(text):
            score += weight
    return min(score, cap)


def score_title(title: str, url: str = "") -> int:
    """Three-bucket scoring: seniority / function / domain, each independently capped."""
    clean_title = canonicalize_title(title)
    text = f"{clean_title} {url}".lower()
    seniority = _bucket_score(text, SENIORITY_PATTERNS, cap=5)
    function  = _bucket_score(text, FUNCTION_PATTERNS,  cap=8)
    domain    = _bucket_score(text, DOMAIN_PATTERNS,    cap=10)
    raw = seniority + function + domain
    if JUNIOR_TOKENS.search(clean_title) and domain < 4 and function < 4:
        return 0
    return raw


def is_garbage_title(title: str) -> bool:
    """True if the title looks like nav/page noise rather than a real job."""
    t = canonicalize_title(title)
    if not t or len(t) < 4:
        return True
    if GARBAGE_TITLE_PATTERNS.match(t):
        return True
    if t.startswith("http") or t.startswith("/") or t.startswith("?"):
        return True
    # Bare hash-like IDs (e.g. Fugro R0030250)
    if re.match(r"^[A-Z0-9_\-]{6,20}$", t):
        return True
    return False


def normalise_title(title: str) -> str:
    """Lowercase + strip punctuation for dedup comparison."""
    t = canonicalize_title(title).lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ─────────────────────────────────────────────────────────────────────────────
# URL + TITLE CANONICALIZATION
# ─────────────────────────────────────────────────────────────────────────────

# Aggregator roots and location-browse indexes: pages that pass the "/jobs"
# style indicators but are never a single posting, so they pollute the digest
# and can never be scored downstream. Mirrors AGGREGATOR_PATTERNS in
# paul-job-pipeline/pipeline/jd_fetcher.py -- keep the two lists in sync.
JUNK_LISTING_PATTERNS = [
    re.compile(r"^https?://(www\.)?climatebase\.org/jobs/?([?#].*)?$", re.I),
    re.compile(r"^https?://(www\.)?climatebase\.org/?([?#].*)?$", re.I),
    re.compile(r"^https?://(www\.)?geo-careers\.com/?([?#].*)?$", re.I),
    re.compile(r"^https?://(www\.)?climatechangejobs\.com/jobs/in-", re.I),
    re.compile(r"^https?://(www\.)?climatechangejobs\.com/?([?#].*)?$", re.I),
    re.compile(r"^https?://(www\.)?trimble\.com/(en/)?careers/?([?#].*)?$", re.I),
    re.compile(r"^https?://careers\.trimble\.com/?([?#].*)?$", re.I),
    re.compile(r"^https?://jobsincarbon\.com/?([?#].*)?$", re.I),
    re.compile(r"^https?://(www\.)?schmidtmarine\.org/?([?#].*)?$", re.I),
]

# /jobs/123/apply is the application form for /jobs/123 -- the posting is one
# path segment up. Rewritten (not dropped) in canonicalize_url so the apply
# link and its JD-page sibling hash to the same id and dedupe.
APPLY_SUFFIX_RE = re.compile(r"(/jobs/\d+)/apply/?$", re.I)


def is_junk_listing_url(url: str) -> bool:
    return any(p.search(url or "") for p in JUNK_LISTING_PATTERNS)


def canonicalize_url(url: str) -> str:
    """Strip tracking params and normalize URL before hashing or storing."""
    if not url:
        return ""
    url = urldefrag(url.strip())[0]
    p = urlparse(url)
    scheme = (p.scheme or "https").lower()
    netloc = p.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = re.sub(r"/{2,}", "/", p.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    m = APPLY_SUFFIX_RE.search(path)
    if m:
        path = path[:m.end(1)]
    kept = []
    for k, v in parse_qsl(p.query, keep_blank_values=False):
        kl = k.lower()
        if kl in TRACKING_PARAM_EXACT:
            continue
        if any(kl.startswith(prefix) for prefix in TRACKING_PARAM_PREFIXES):
            continue
        kept.append((k, v))
    query = urlencode(sorted(kept))
    return urlunparse((scheme, netloc, path, "", query, ""))


def _strip_title_separators(text: str) -> str:
    for sep in [" | ", " :: ", " · ", " @ "]:
        if sep in text:
            left = text.split(sep)[0].strip()
            if len(left) >= 4:
                return left
    return text.strip()


def _maybe_strip_dash_suffix(text: str) -> str:
    if " - " not in text:
        return text
    parts = [p.strip() for p in text.split(" - ") if p.strip()]
    if len(parts) < 2:
        return text
    last = parts[-1].lower()
    if last in REMOTE_WORDS:
        return " - ".join(parts[:-1]).strip()
    if re.fullmatch(r"[A-Za-z .]{2,30}", parts[-1]) and len(parts[-1].split()) <= 4:
        return " - ".join(parts[:-1]).strip()
    return text


def canonicalize_title(title: str) -> str:
    """Strip location tags, remote suffixes, and pipe/separator junk from job titles."""
    t = re.sub(r"\s+", " ", (title or "").strip())
    t = _strip_title_separators(t)
    prev = None
    while t and prev != t:
        prev = t
        t = re.sub(
            r"\s*\((remote|hybrid|onsite|usa?|united states|north america|europe|"
            r"uk|united kingdom|canada|global|multiple locations|various locations|m/f/d|f/m/d)\)\s*$",
            "", t, flags=re.I,
        )
        t = _maybe_strip_dash_suffix(t)
        t = re.sub(
            r"\s*[,|/]\s*(remote|hybrid|onsite|usa?|united states|north america|europe|"
            r"uk|united kingdom|canada|global|multiple locations|various locations)\s*$",
            "", t, flags=re.I,
        )
    t = re.sub(r"\s*[,|/-]\s*$", "", t).strip()
    return t


def parse_dt(value: str | None) -> datetime | None:
    """Parse an ISO or RFC-2822 datetime string to a UTC-aware datetime."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


# utilities (session, sha, load/save)

def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def _build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=2,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "HEAD"]),
        raise_on_status=False,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session


SESSION = _build_session()
HTML_CACHE: dict[str, str] = {}
TITLE_CACHE: dict[str, str] = {}

# Concurrency. The per-company scrape used to run sequentially over 525
# companies, which is the 2+ hour runtime. Pass A (requests-based: the *_api
# adapters + the fast Pass-1 of html_links) is I/O-bound and parallelises
# safely on the shared thread-safe Session. Playwright (Pass B) defaults to
# sequential because the sync API is not thread-safe; bump PLAYWRIGHT_WORKERS
# only with a process pool.
MAX_SCRAPE_WORKERS = int(os.environ.get("SCRAPE_WORKERS", "16"))
MAX_PLAYWRIGHT_WORKERS = int(os.environ.get("PLAYWRIGHT_WORKERS", "1"))


class _DeferToPlaywright(Exception):
    """Raised by get_html_links(defer_playwright=True) when Pass 1 wants to
    escalate, so the parallel orchestrator can batch the slow Playwright work
    into a separate (bounded) phase instead of blocking a fast worker."""


def load_health() -> dict:
    """Per-company scrape health: makes 'succeeded but found nothing forever'
    visible instead of indistinguishable from a healthy quiet board."""
    if os.path.exists(HEALTH_FILE):
        with open(HEALTH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_health(health: dict) -> None:
    with open(HEALTH_FILE, "w", encoding="utf-8") as f:
        json.dump(health, f, indent=1, sort_keys=True)


def update_health(health: dict, name: str, status: str, n_items: int = 0) -> None:
    """status: 'ok' or 'err'. Streak counters are consecutive daily runs."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    h = health.setdefault(name, {"first_tracked": today, "runs": 0,
                                 "empty_streak": 0, "fail_streak": 0})
    h["runs"] = h.get("runs", 0) + 1
    if status == "err":
        h["fail_streak"] = h.get("fail_streak", 0) + 1
        return
    h["last_ok"] = today
    h["fail_streak"] = 0
    if n_items > 0:
        h["last_nonempty"] = today
        h["empty_streak"] = 0
    else:
        h["empty_streak"] = h.get("empty_streak", 0) + 1


def build_attention_list(health: dict, active_names: set[str]) -> list[str]:
    """Boards that need a human look, worst first."""
    out = []
    for name in sorted(active_names):
        h = health.get(name)
        if not h:
            continue
        if h.get("fail_streak", 0) >= FAIL_ATTENTION_STREAK:
            out.append(f"{name}: scrape FAILING {h['fail_streak']} runs in a row")
        elif h.get("last_nonempty") and h.get("empty_streak", 0) >= EMPTY_ATTENTION_STREAK:
            out.append(f"{name}: zero items for {h['empty_streak']} runs "
                       f"(last produced {h['last_nonempty']}); verify the board moved or died")
        elif not h.get("last_nonempty") and h.get("runs", 0) >= NEW_BOARD_GRACE_RUNS:
            out.append(f"{name}: never produced a single item in {h['runs']} runs "
                       f"since {h.get('first_tracked', '?')}; URL or type is probably wrong")
    return out


def load_seen() -> dict:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_seen(seen: dict) -> None:
    # Atomic write: a crash mid-rewrite of seen_jobs.json (now ~5 MB) would
    # otherwise truncate prod state. Tempfile + os.replace makes the swap
    # atomic on the same filesystem.
    tmp = SEEN_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(seen, f, indent=2, sort_keys=True)
    os.replace(tmp, SEEN_FILE)


def fetch_html(url: str, timeout: int = 30) -> str:
    """Fetch a URL via the shared session (retries handled by HTTPAdapter)."""
    cu = canonicalize_url(url)
    if cu in HTML_CACHE:
        return HTML_CACHE[cu]
    r = SESSION.get(cu, timeout=timeout)
    r.raise_for_status()
    html = r.text
    HTML_CACHE[cu] = html
    return html


# ─────────────────────────────────────────────────────────────────────────────
# SPECIAL SITE DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def is_notion_url(url: str) -> bool:
    """Notion public pages are JavaScript-rendered and cannot be scraped."""
    u = url.lower()
    return "notion.site" in u or "notion.so" in u


def is_linkedin_url(url: str) -> bool:
    return "linkedin.com" in url.lower()


# ─────────────────────────────────────────────────────────────────────────────
# LINK EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

REJECT_SUBSTRINGS = [
    "linkedin.com", "facebook.com", "twitter.com", "x.com",
    "youtube.com", "instagram.com", "glassdoor.com",
    "privacy", "terms", "cookie", "legal", "contact",
    ".pdf", ".png", ".jpg", ".gif", ".svg", ".css", ".js",
    "mailto:", "tel:", "javascript:",
    "/login", "/signup", "/register",
    "share=", "ref=", "utm_",
]

JOB_INDICATORS = [
    "/apply/", "/jobs/", "/job/", "/positions/", "/openings/",
    "/vacancies/", "/careers/", "/career/", "/opportunities/",
    "/role/", "/roles/", "/posting/", "/postings/",
    "/recruitment/", "/jobdetail/", "/job-details/",
    "/jobs/view/", "/job-description/", "/work-with-us/", "/join-us/",
    "/o/", "/j/",
    "jobs.lever.co/", "jobs.ashbyhq.com/", "greenhouse.io/",
    "job-boards.greenhouse.io/", "job-boards.eu.greenhouse.io/",
    "boards.greenhouse.io/", "apply.workable.com/", "applytojob.com/apply/",
    "bamboohr.com/careers", "myworkdayjobs.com/", "recruitee.com/o/",
    "personio.de/job/", "personio.com/job/", "factorial.it/", "hrmos.co/",
    "smartrecruiters.com/", "icims.com/", "teamtailor.com/",
    "careers.team/", "pinpointhq.com/", "rippling.com/", "breezy.hr/",
    "gohire.io/", "gusto.com/boards/", "paylocity.com/recruiting/",
    "hibob.com/jobs", "zohorecruit.com/jobs/", "comeet.com/jobs/",
]

BOARD_HOSTS = [
    "jobs.lever.co/", "jobs.ashbyhq.com/", "apply.workable.com/",
    "job-boards.eu.greenhouse.io/", "job-boards.greenhouse.io/",
    "boards.greenhouse.io/", "greenhouse.io/", "bamboohr.com/careers",
    "myworkdayjobs.com/", "personio.de/", "personio.com/", "recruitee.com/",
    "factorial.it/", "hrmos.co/", "smartrecruiters.com/", "icims.com/",
    "teamtailor.com/", "applytojob.com/", "careers.team/",
    "pinpointhq.com/", "breezy.hr/", "gohire.io/", "gusto.com/boards/",
    "paylocity.com/recruiting/",
]


def extract_links(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#"):
            continue
        hlow = href.lower()
        if any(x in hlow for x in ["mailto:", "tel:", "javascript:"]):
            continue
        full = urljoin(base_url, href)
        full = urldefrag(full)[0]
        u = full.lower()
        if any(x in u for x in REJECT_SUBSTRINGS):
            continue
        if is_junk_listing_url(full):
            continue
        if "jobs.lever.co/" in u and "?" in u:
            path = u.split("jobs.lever.co/", 1)[1]
            if path.count("/") < 1:
                continue
        if any(ind in u for ind in JOB_INDICATORS):
            links.add(full)
    return links


def find_next_page_links(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    candidates: set[str] = set()
    next_patterns = re.compile(
        r"\bnext\b|\bnext\s*page\b|load\s*more|show\s*more|page\s*\d",
        re.IGNORECASE,
    )
    for a in soup.find_all("a", href=True):
        text = (a.get_text(" ", strip=True) + " " + a.get("aria-label", "")).strip()
        if next_patterns.search(text):
            href = a["href"].strip()
            if href and not href.startswith("#"):
                candidates.add(urljoin(base_url, href))
    return candidates


def pagination_urls(base_url: str) -> list[str]:
    sep = "&" if "?" in base_url else "?"
    b = base_url.rstrip("/")
    return [
        f"{base_url}{sep}page=2", f"{base_url}{sep}page=3",
        f"{base_url}{sep}paged=2", f"{base_url}{sep}paged=3",
        f"{base_url}{sep}offset=20", f"{base_url}{sep}offset=40",
        f"{b}/page/2", f"{b}/page/3",
        f"{b}/jobs", f"{b}/jobs?page=2", f"{b}/careers?page=2",
    ]


def is_board_url(url: str) -> bool:
    u = url.lower()
    return any(b in u for b in BOARD_HOSTS)


# ─────────────────────────────────────────────────────────────────────────────
# GARBAGE DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def looks_like_garbage(items: list[dict]) -> bool:
    """
    Returns True if what we scraped looks like navigation noise.
    Triggers Pass 2 (Playwright).

    Heuristics:
    - Fewer than 2 items
    - More than 60% of titles match GARBAGE_TITLE_PATTERNS
    - All titles are identical (e.g. 40x "Synspective")
    """
    if not items or len(items) < 2:
        return True

    titles = [i.get("title") or "" for i in items]

    unique_titles = set(normalise_title(t) for t in titles if t)
    if len(unique_titles) == 1:
        return True

    garbage_count = sum(1 for t in titles if is_garbage_title(t))
    if garbage_count / len(titles) > 0.60:
        return True

    return False


# JS-heavy site patterns (go straight to Playwright, no Pass 1)

JS_HEAVY_PATTERNS = [
    "myworkdayjobs.com", "wd1.myworkdaysite.com", "wd3.myworkdaysite.com",
    "wd5.myworkdayjobs.com", "workforcenow.adp.com", "ats.rippling.com",
    "csod.com",
    # Getro-powered VC portfolio boards — go straight to Playwright + intercept
    "jobs.dcvc.com", "jobs.energyimpactpartners.com", "jobs.g2vp.com",
    "jobs.obvious.com", "jobs.aenu.com", "jobs.atoneventures.com",
    "jobs.cleanenergyventures.com", "jobs.preludeventures.com",
    "jobs.s2gventures.com", "jobs.galvanizeclimate.com",
    "jobs.breakthroughenergy.org", "jobs.pale.blue", "jobs.overture.vc",
    "jobs.planet-a.com", "jobs.convectivecapital.com",
    "jobs.elementalimpact.com", "jobs.mcj.vc", "jobs.thirdsphere.com",
    "jobs.systemiq.earth", "jobs.worldfund.vc", "jobs.2150.vc",
    "careers.voyagervc.com", "careers.extantia.com",
    "techjobs.sosv.com", "jobs.congruentvc.com",
]


def is_js_heavy(url: str) -> bool:
    u = url.lower()
    return any(p in u for p in JS_HEAVY_PATTERNS)


# ─────────────────────────────────────────────────────────────────────────────
# PLAYWRIGHT SCRAPER (Pass 2)
# ─────────────────────────────────────────────────────────────────────────────

def get_playwright_links(company: dict) -> list[dict]:
    """
    Full Playwright scrape with two strategies:
    1. Intercept JSON API responses that contain job data (Getro VC portfolio
       boards, Synspective, Workday variants, custom ATS, etc.). Accumulates
       across multiple paginated responses and dedupes by title+url.
    2. Fall back to rendering the page and extracting <a> links.

    For Getro-style boards (jobs.{vc}.com) and other paginated APIs, scrolls
    aggressively to trigger pagination of API calls. Catches API responses
    even when the URL doesn't include obvious 'job' keywords by also matching
    Getro/board-specific patterns.
    """
    try:
        from playwright.sync_api import sync_playwright

        url = company["url"]
        intercepted_jobs: list[dict] = []
        seen_keys: set = set()

        # Detect Getro/portfolio-board patterns; scroll harder for these
        ulow = url.lower()
        is_paginated_board = (
            ulow.startswith("https://jobs.") or
            ulow.startswith("https://careers.") or
            "getro" in ulow or
            "/jobs" in ulow.rstrip("/")
        )

        # Broader keyword filter: include getro, talent, boards, listings,
        # collections, search — covers Getro API and similar portfolio platforms
        URL_KEYWORDS = [
            "job", "position", "career", "posting", "opening",
            "vacancy", "recruit", "jobs", "offer",
            "getro", "talent", "boards", "listings",
            "collections", "search", "openings",
        ]

        # Container keys to walk in JSON responses (top-level and one nested level)
        CONTAINER_KEYS = [
            "jobs", "positions", "postings", "results",
            "data", "items", "offers", "vacancies",
            "listings", "openings", "hits", "records",
        ]

        TITLE_FIELDS = ["title", "name", "jobTitle", "position", "job_title", "text"]
        URL_FIELDS = ["absolute_url", "hostedUrl", "applyUrl", "url", "link",
                      "apply_url", "jobUrl", "shortlink", "href"]

        def extract_from_container(container):
            """Pull jobs out of one container (list of dicts)."""
            if not container or not isinstance(container, list) or len(container) == 0:
                return
            sample = container[0]
            if not isinstance(sample, dict):
                return
            tf = next((k for k in TITLE_FIELDS if k in sample), None)
            if not tf:
                return
            uf = next((k for k in URL_FIELDS if k in sample), None)
            for job in container:
                if not isinstance(job, dict):
                    continue
                t = job.get(tf, "")
                u = job.get(uf, "") if uf else ""
                if not t:
                    continue
                # Filter rejected URLs
                if u and any(x in str(u).lower() for x in
                             ["linkedin.com", "facebook.com", "glassdoor.com"]):
                    continue
                key = f"{str(t).strip()}|{str(u).strip()}"
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                intercepted_jobs.append({
                    "id": sha(company["name"] + "|intercepted|" + str(t) + str(u)),
                    "url": u or url,
                    "title": str(t),
                })

        def handle_response(response):
            try:
                ctype = response.headers.get("content-type", "")
                if "json" not in ctype:
                    return
                rurl = response.url.lower()
                if not any(kw in rurl for kw in URL_KEYWORDS):
                    return
                data = response.json()
                # Walk top-level
                if isinstance(data, list):
                    extract_from_container(data)
                elif isinstance(data, dict):
                    for k in CONTAINER_KEYS:
                        if k in data:
                            v = data[k]
                            if isinstance(v, list):
                                extract_from_container(v)
                    # Walk one level nested (data.results.jobs etc.)
                    for outer_k in ["data", "results", "payload"]:
                        outer = data.get(outer_k)
                        if isinstance(outer, dict):
                            for k in CONTAINER_KEYS:
                                if k in outer and isinstance(outer[k], list):
                                    extract_from_container(outer[k])
            except Exception:
                pass

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("response", handle_response)
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            # Aggressive scrolling for paginated boards (Getro typically loads
            # 50 jobs per page; need 5-10 scrolls to capture 250-500 jobs)
            scroll_count = 10 if is_paginated_board else 3
            for _ in range(scroll_count):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1200)
            # Final settle for any pending responses
            page.wait_for_timeout(2500)
            html = page.content()
            browser.close()

        if intercepted_jobs:
            log.info(f"  {company['name']}: intercepted {len(intercepted_jobs)} jobs from API")
            return intercepted_jobs

        links = extract_links(html, url)
        if links:
            return [
                {"id": sha(company["name"] + "|" + l), "url": l, "title": None}
                for l in sorted(links)
            ]

        log.warning(f"  {company['name']}: Playwright found nothing – site may need manual check")
        return []

    except ImportError:
        log.warning("Playwright not installed – skipping JS site: " + company["name"])
        return []
    except Exception as e:
        log.warning(f"Playwright failed for {company['name']}: {e}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# PER-TYPE SCRAPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_html_links(company: dict, defer_playwright: bool = False) -> list[dict]:
    """
    Two-pass scraper:
    Pass 1 – fast requests + BS4.
    Pass 2 – Playwright, triggered if:
      - Pass 1 finds fewer than MIN_LINK_THRESHOLD links, OR
      - the sampled titles look like garbage.

    Special cases handled before scraping:
      - LinkedIn URLs: warn and skip (requires login, scraping blocked).
      - Notion pages: warn and skip (JS-rendered, no public API).
    """
    base_url = company["url"]
    name = company["name"]

    # ── Special-case: LinkedIn ────────────────────────────────────────────
    if is_linkedin_url(base_url):
        log.warning(
            f"  {name}: LinkedIn URL detected. LinkedIn blocks scrapers and requires "
            f"login. Replace this URL in companies.yaml with the company's direct "
            f"ATS URL (Greenhouse, Lever, Workable, etc.) for reliable results."
        )
        return []

    # ── Special-case: Notion ──────────────────────────────────────────────
    if is_notion_url(base_url):
        log.warning(
            f"  {name}: Notion page detected. Notion public pages are fully "
            f"JavaScript-rendered and cannot be scraped with requests or Playwright. "
            f"Find this company's ATS URL directly (check their job posts for "
            f"an apply link to Greenhouse/Lever/Ashby/etc.) and update companies.yaml."
        )
        return []

    # ── Known JS-heavy ATS: skip Pass 1 entirely ─────────────────────────
    if is_js_heavy(base_url):
        log.info(f"  {name}: known JS-heavy site, going straight to Playwright")
        if defer_playwright:
            raise _DeferToPlaywright()
        pw_items = get_playwright_links(company)
        if company.get("link_contains"):
            needle = company["link_contains"]
            pw_items = [i for i in pw_items if needle in i.get("url", "")]
        return pw_items

    # ── Pass 1: requests + BS4 ────────────────────────────────────────────
    # Fetch the base URL first; only attempt pagination if it succeeds.
    links: set[str] = set()
    fetched: set[str] = set()
    base_ok = False

    try:
        html = fetch_html(base_url)
        fetched.add(base_url)
        base_ok = True
        links |= extract_links(html, base_url)
        # Follow real "next page" links found on the page
        for np in find_next_page_links(html, base_url):
            if np not in fetched and len(fetched) < 6:
                try:
                    np_html = fetch_html(np)
                    links |= extract_links(np_html, np)
                    fetched.add(np)
                except Exception:
                    pass
    except Exception:
        pass

    # Only try speculative pagination if the base URL succeeded
    if base_ok:
        for page_url in pagination_urls(base_url):
            if page_url in fetched:
                continue
            try:
                html = fetch_html(page_url, timeout=15)
                fetched.add(page_url)
                links |= extract_links(html, page_url)
            except Exception:
                pass

    # Follow links to known ATS board pages found in the results
    board_links = sorted({l for l in links if is_board_url(l) and l != base_url})
    for board_url in board_links[:3]:
        try:
            board_html = fetch_html(board_url)
            links |= extract_links(board_html, board_url)
        except Exception:
            pass

    if company.get("link_contains"):
        needle = company["link_contains"]
        links = {l for l in links if needle in l}

    pass1_items = [
        {"id": sha(name + "|" + l), "url": l, "title": None}
        for l in sorted(links)
    ]

    # ── Escalation check 1: too few links ────────────────────────────────
    if len(pass1_items) < MIN_LINK_THRESHOLD:
        log.info(
            f"  {name}: Pass 1 found only {len(pass1_items)} link(s) "
            f"(threshold: {MIN_LINK_THRESHOLD}) – escalating to Playwright"
        )
        if defer_playwright:
            raise _DeferToPlaywright()
        pw_items = get_playwright_links(company)
        if company.get("link_contains"):
            needle = company["link_contains"]
            pw_items = [i for i in pw_items if needle in i.get("url", "")]
        return pw_items

    # ── Escalation check 2: titles look like garbage ──────────────────────
    sampled = pass1_items[:5]
    for item in sampled:
        if item["title"] is None:
            item["title"] = fetch_title(item["url"])

    if looks_like_garbage(sampled):
        log.info(
            f"  {name}: Pass 1 titles look like noise – escalating to Playwright"
        )
        if defer_playwright:
            raise _DeferToPlaywright()
        pw_items = get_playwright_links(company)
        if company.get("link_contains"):
            needle = company["link_contains"]
            pw_items = [i for i in pw_items if needle in i.get("url", "")]
        return pw_items

    return pass1_items


def get_greenhouse_jobs(company: dict) -> list[dict]:
    board = company.get("board")
    url = company.get("url", "")
    # The standard board API host serves all boards, including EU-rendered ones.
    if board:
        gh_url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    elif "boards-api.greenhouse.io" in url:
        gh_url = url
    else:
        raise ValueError("Greenhouse: missing 'board' key")

    r = SESSION.get(gh_url, timeout=45)
    r.raise_for_status()
    data = r.json()

    results = []
    for job in data.get("jobs", []):
        job_url = canonicalize_url(job.get("absolute_url") or job.get("url") or "")
        title = canonicalize_title(job.get("title") or "")
        job_id = job.get("id") or sha(job_url or title)
        if not job_url:
            continue
        results.append(
            {"id": sha(company["name"] + "|" + str(job_id)), "url": job_url, "title": title}
        )
    return results


def get_lever_jobs(company: dict) -> list[dict]:
    lever_company = company.get("lever_company")
    url = company.get("url", "")
    if not lever_company:
        if "jobs.lever.co/" in url:
            lever_company = url.split("jobs.lever.co/", 1)[1].split("/", 1)[0].strip()
        else:
            raise ValueError("Lever: missing 'lever_company' key")

    api_url = f"https://api.lever.co/v0/postings/{lever_company}?mode=json"
    r = SESSION.get(api_url, timeout=45)
    r.raise_for_status()
    data = r.json()

    results = []
    for job in data:
        job_url = canonicalize_url(job.get("hostedUrl") or job.get("applyUrl") or "")
        title = canonicalize_title(job.get("text") or job.get("title") or "")
        job_id = job.get("id") or sha(job_url or title)
        if not job_url:
            continue
        results.append(
            {"id": sha(company["name"] + "|" + str(job_id)), "url": job_url, "title": title}
        )
    return results


def get_workable_jobs(company: dict) -> list[dict]:
    account = company.get("workable_account")
    url = company.get("url", "")
    if not account:
        if "apply.workable.com/" in url:
            account = url.split("apply.workable.com/", 1)[1].split("/", 1)[0].strip()
        else:
            raise ValueError("Workable: missing 'workable_account' key")

    # v1 widget endpoint: the only Workable listing API that answers GET.
    # (v3 accounts/{slug}/jobs is POST-only and 404s on GET, which made every
    # workable_api company silently return zero for months.)
    api_url = f"https://apply.workable.com/api/v1/widget/accounts/{account}?details=false"
    r = SESSION.get(api_url, timeout=45)
    r.raise_for_status()
    data = r.json()
    results = []
    for job in data.get("jobs", []):
        job_url = canonicalize_url(job.get("shortlink") or job.get("url") or "")
        title = canonicalize_title(job.get("title") or "")
        job_id = job.get("shortcode") or sha(job_url or title)
        if not job_url:
            continue
        results.append(
            {"id": sha(company["name"] + "|" + str(job_id)), "url": job_url, "title": title}
        )
    return results


def get_ashby_jobs(company: dict) -> list[dict]:
    r = SESSION.get(company["url"], timeout=45)
    r.raise_for_status()
    data = r.json()
    results = []
    for job in data.get("jobs", []):
        job_url = canonicalize_url(job.get("jobUrl") or "")
        if not job_url:
            continue
        job_id = job.get("id") or sha(job_url)
        results.append({
            "id": sha(company["name"] + "|" + str(job_id)),
            "url": job_url,
            "title": canonicalize_title(job.get("title") or ""),
        })
    return results


def get_recruitee_jobs(company: dict) -> list[dict]:
    """Recruitee public offers API: {sub}.recruitee.com/api/offers/"""
    url = company.get("url", "")
    sub = company.get("recruitee_company")
    if not sub:
        m = re.search(r"https?://([^.]+)\.recruitee\.com", url)
        if not m:
            raise ValueError("Recruitee: cannot determine subdomain from URL")
        sub = m.group(1)
    r = SESSION.get(f"https://{sub}.recruitee.com/api/offers/", timeout=45)
    r.raise_for_status()
    results = []
    for job in r.json().get("offers", []):
        job_url = canonicalize_url(job.get("careers_url") or job.get("careers_apply_url") or "")
        if not job_url:
            continue
        job_id = job.get("id") or sha(job_url)
        results.append({
            "id": sha(company["name"] + "|" + str(job_id)),
            "url": job_url,
            "title": canonicalize_title(job.get("title") or ""),
        })
    return results


def get_rippling_jobs(company: dict) -> list[dict]:
    """Rippling public board API: api.rippling.com/platform/api/ats/v1/board/{slug}/jobs.
    The slug is the path segment in ats.rippling.com/{slug}/jobs (locale prefixes stripped)."""
    slug = company.get("board")
    if not slug:
        path = urlparse(company.get("url", "")).path.strip("/").split("/")
        # drop a leading locale segment like "en" or "en-US", then take the board slug
        if path and re.fullmatch(r"[a-z]{2}([_-][A-Za-z]{2,4})?", path[0]) and len(path) > 1:
            path = path[1:]
        if not path or not path[0] or path[0] == "jobs":
            raise ValueError("Rippling: could not derive board slug from url")
        slug = path[0]
    r = SESSION.get(f"https://api.rippling.com/platform/api/ats/v1/board/{slug}/jobs", timeout=45)
    r.raise_for_status()
    results = []
    for job in r.json():
        job_url = canonicalize_url(job.get("url") or "")
        if not job_url:
            continue
        job_id = job.get("uuid") or sha(job_url)
        results.append({
            "id": sha(company["name"] + "|" + str(job_id)),
            "url": job_url,
            "title": canonicalize_title(job.get("name") or ""),
        })
    return results


def get_bamboohr_jobs(company: dict) -> list[dict]:
    """BambooHR public careers JSON: {sub}.bamboohr.com/careers/list"""
    url = company.get("url", "")
    sub = company.get("bamboohr_account")
    if not sub:
        m = re.search(r"https?://([^.]+)\.bamboohr\.com", url)
        if not m:
            raise ValueError("BambooHR: cannot determine subdomain from URL")
        sub = m.group(1)
    r = SESSION.get(f"https://{sub}.bamboohr.com/careers/list", timeout=45,
                    headers={"Accept": "application/json"})
    r.raise_for_status()
    results = []
    for job in r.json().get("result", []):
        job_id = job.get("id")
        if job_id is None:
            continue
        job_url = canonicalize_url(f"https://{sub}.bamboohr.com/careers/{job_id}")
        results.append({
            "id": sha(company["name"] + "|" + str(job_id)),
            "url": job_url,
            "title": canonicalize_title(job.get("jobOpeningName") or ""),
        })
    return results


def get_workday_jobs(company: dict) -> list[dict]:
    """Workday CXS JSON API. Parses tenant + site from a myworkdayjobs URL
    (https://{tenant}.{dc}.myworkdayjobs.com/[{lang}/]{site}) and pages through
    the jobs endpoint. Replaces the slow Playwright path for Workday sites."""
    url = company.get("url", "")
    m = re.match(
        r"https?://([^/]*\.myworkdayjobs\.com)/(?:([a-zA-Z]{2}-[A-Z]{2})/)?([^/?#]+)",
        url,
    )
    if not m:
        raise ValueError("Workday: cannot parse host/site from URL")
    host, lang, site = m.group(1), m.group(2), m.group(3)
    tenant = host.split(".")[0]
    cxs = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    lang_seg = f"{lang}/" if lang else ""

    results: list[dict] = []
    seen_paths: set[str] = set()
    offset, limit, total = 0, 20, None
    while True:
        r = SESSION.post(
            cxs,
            json={"appliedFacets": {}, "limit": limit, "offset": offset, "searchText": ""},
            timeout=45,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        r.raise_for_status()
        data = r.json()
        if total is None:
            total = data.get("total", 0)
        postings = data.get("jobPostings", [])
        if not postings:
            break
        for job in postings:
            path = job.get("externalPath") or ""
            if not path or path in seen_paths:
                continue
            seen_paths.add(path)
            job_url = canonicalize_url(f"https://{host}/{lang_seg}{site}{path}")
            results.append({
                "id": sha(company["name"] + "|" + path),
                "url": job_url,
                "title": canonicalize_title(job.get("title") or ""),
            })
        offset += limit
        if offset >= (total or 0) or offset > 2000:  # safety cap
            break
    return results


def _extract_jsonld_title(soup: BeautifulSoup) -> str:
    """Pull job title from JSON-LD structured data if present."""
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text(strip=True)
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue
        stack = data if isinstance(data, list) else [data]
        for obj in stack:
            if isinstance(obj, dict):
                if obj.get("@type") == "JobPosting" and obj.get("title"):
                    return str(obj["title"]).strip()
                for entry in obj.get("@graph", []):
                    if isinstance(entry, dict) and entry.get("@type") == "JobPosting" and entry.get("title"):
                        return str(entry["title"]).strip()
    return ""


def fetch_title(url: str) -> str:
    """Fetch and return a cleaned job title, trying JSON-LD before falling back to HTML tags."""
    cu = canonicalize_url(url)
    if not cu:
        return ""
    if cu in TITLE_CACHE:
        return TITLE_CACHE[cu]
    title = ""
    try:
        r = SESSION.get(cu, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # 1. JSON-LD structured data (most accurate for ATS pages)
        title = _extract_jsonld_title(soup)
        # 2. OpenGraph / twitter meta tags
        if not title:
            for attrs in ({"property": "og:title"}, {"name": "twitter:title"}, {"name": "title"}):
                tag = soup.find("meta", attrs=attrs)
                if tag and tag.get("content"):
                    title = tag["content"].strip()
                    break
        # 3. Heading tags
        if not title:
            for selector in ("h1", "h2"):
                tag = soup.select_one(selector)
                if tag:
                    text = tag.get_text(" ", strip=True)
                    if text:
                        title = text
                        break
        # 4. <title> tag as last resort
        if not title and soup.title and soup.title.string:
            title = soup.title.string.strip()
        title = canonicalize_title(title)
    except Exception:
        title = ""
    TITLE_CACHE[cu] = title
    return title


def batch_fetch_titles(items: list[dict], max_workers: int = 20) -> None:
    """Fetch titles for all items missing one, concurrently.

    Mutates items in-place. Items that already have a title are skipped.
    Uses a thread pool so 20 HTTP requests fire simultaneously instead of
    one at a time -- the primary fix for the 2+ hour runtime problem.
    """
    needs_title = [item for item in items if not item.get("title") and item.get("url")]
    if not needs_title:
        return

    log.info(f"  Fetching {len(needs_title)} titles concurrently (workers={max_workers})")

    def _fetch(item: dict) -> tuple[dict, str]:
        return item, fetch_title(item["url"])

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch, item): item for item in needs_title}
        for future in as_completed(futures):
            try:
                item, title = future.result()
                item["title"] = title
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# DEDUPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def deduplicate(items: list[dict]) -> list[dict]:
    """
    Within a single company's results, collapse duplicate job titles
    (same normalised title seen on multiple boards) to first occurrence.
    """
    seen_norm: dict[str, bool] = {}
    out: list[dict] = []
    for item in items:
        title = item.get("title") or ""
        norm = normalise_title(title)
        key = item["company"] + "|" + norm
        if norm and key in seen_norm:
            continue
        if norm:
            seen_norm[key] = True
        out.append(item)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY SEARCH SWEEP
# ─────────────────────────────────────────────────────────────────────────────
#
# Runs once per week (checks a local cache file for last run date).
# Searches a handful of ATS board domains for relevant roles in the EO /
# geospatial / maritime / BD space that aren't from companies already in
# your YAML watchlist.
#
# Requires the `googlesearch-python` package:
#   pip install googlesearch-python
#
# If the package isn't installed the sweep is silently skipped and a
# warning is logged. No hard dependency.
# ─────────────────────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    # Earth observation / satellite / geospatial
    'site:jobs.lever.co "earth observation" "business development"',
    'site:jobs.lever.co "satellite" "partnerships"',
    'site:jobs.lever.co "geospatial" "director"',
    'site:jobs.ashbyhq.com "earth observation" "business development"',
    'site:jobs.ashbyhq.com "satellite" "partnerships"',
    'site:boards.greenhouse.io "earth observation" "sales"',
    'site:boards.greenhouse.io "geospatial" "partnerships"',
    'site:jobs.lever.co "remote sensing" "commercial"',
    'site:jobs.ashbyhq.com "geospatial" "head of commercial"',
    'site:job-boards.greenhouse.io "satellite data" "director"',
    'site:job-boards.greenhouse.io "geospatial" "business development"',
    'site:apply.workable.com "earth observation" "partnerships"',
    'site:apply.workable.com "satellite" "director"',
    # Maritime / ocean
    'site:jobs.lever.co "maritime" "business development"',
    'site:jobs.lever.co "maritime" "director"',
    'site:boards.greenhouse.io "maritime" "partnerships"',
    'site:job-boards.greenhouse.io "maritime" "commercial"',
    'site:jobs.lever.co "ocean" "business development"',
    'site:jobs.ashbyhq.com "maritime" "head of"',
    # Climate / carbon / ESG
    'site:jobs.lever.co "climate" "partnerships" "director"',
    'site:jobs.lever.co "carbon" "business development"',
    'site:boards.greenhouse.io "climate risk" "director"',
    'site:job-boards.greenhouse.io "sustainability" "partnerships"',
    'site:jobs.ashbyhq.com "climate" "commercial"',
    'site:apply.workable.com "climate" "business development"',
    # Supply chain / trade intelligence
    'site:jobs.lever.co "supply chain" "partnerships"',
    'site:boards.greenhouse.io "trade intelligence" "director"',
    'site:job-boards.greenhouse.io "supply chain visibility" "director"',
    # Data licensing / commercialization
    'site:jobs.lever.co "data licensing"',
    'site:boards.greenhouse.io "data licensing"',
    'site:jobs.lever.co "data commercialization"',
    'site:job-boards.greenhouse.io "data partnerships" "director"',
]


def _load_search_cache() -> dict:
    if os.path.exists(SEARCH_CACHE_FILE):
        with open(SEARCH_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_search_cache(cache: dict) -> None:
    tmp = SEARCH_CACHE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
    os.replace(tmp, SEARCH_CACHE_FILE)


def run_weekly_search_sweep(known_companies: list[dict]) -> list[dict]:
    """
    Runs Google searches against ATS boards to surface roles from companies
    not in your YAML watchlist. Returns a list of new items (same shape as
    main scraper items) to be scored and added to the digest.

    Runs at most once per 7 days (tracked via search_cache.json).
    """
    cache = _load_search_cache()
    last_run_str = cache.get("last_search_sweep")
    if last_run_str:
        last_run = datetime.fromisoformat(last_run_str)
        if datetime.now(timezone.utc) - last_run < timedelta(days=7):
            log.info("Search sweep: last run < 7 days ago, skipping.")
            return []

    try:
        from googlesearch import search as google_search
    except ImportError:
        log.warning(
            "Search sweep skipped: 'googlesearch-python' not installed. "
            "Run: pip install googlesearch-python"
        )
        return []

    known_domains = set()
    for co in known_companies:
        url = co.get("url", "")
        try:
            known_domains.add(urlparse(url).netloc.lower())
        except Exception:
            pass

    seen_urls: set[str] = set(cache.get("seen_search_urls", []))
    sweep_items: list[dict] = []

    for query in SEARCH_QUERIES:
        log.info(f"Search sweep: {query}")
        try:
            results = list(google_search(query, num_results=10, sleep_interval=2))
        except Exception as e:
            log.warning(f"Search sweep query failed: {e}")
            continue

        for url in results:
            if url in seen_urls:
                continue
            seen_urls.add(url)

            # Skip if this URL belongs to a domain already in YAML
            try:
                domain = urlparse(url).netloc.lower()
            except Exception:
                continue
            if any(kd in domain or domain in kd for kd in known_domains):
                continue

            # Derive a company name from the URL path (best-effort)
            parts = url.split("/")
            inferred_name = parts[3] if len(parts) > 3 else domain

            sweep_items.append({
                "id": sha("__sweep__|" + url),
                "url": url,
                "title": None,
                "company": f"[Sweep] {inferred_name}",
            })

        time.sleep(1)

    # Fetch titles for sweep items concurrently
    batch_fetch_titles(sweep_items)

    cache["last_search_sweep"] = datetime.now(timezone.utc).isoformat()
    cache["seen_search_urls"] = list(seen_urls)
    _save_search_cache(cache)

    scored = []
    for item in sweep_items:
        title = item.get("title") or ""
        if is_garbage_title(title):
            continue
        s = score_title(title, item["url"])
        if s > 0:
            item["score"] = s
            scored.append(item)

    log.info(f"Search sweep complete: {len(scored)} relevant new results from {len(sweep_items)} URLs")
    return scored


# ─────────────────────────────────────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────────────────────────────────────

def build_html_email(
    new_items: list[dict],
    errors: list[str],
    run_time: str,
    scrape_summary: str = "",
    manual_check_companies: list[dict] | None = None,
    attention: list[str] | None = None,
) -> str:
    from collections import defaultdict

    by_company: dict[str, list[dict]] = defaultdict(list)
    for item in new_items:
        by_company[item["company"]].append(item)

    sorted_companies = sorted(
        by_company.items(),
        key=lambda kv: max(i["score"] for i in kv[1]),
        reverse=True,
    )

    def score_badge(score: int) -> str:
        if score >= 4:
            colour = "#1a7a3c"; label = f"★ {score}"
        elif score >= 2:
            colour = "#2563eb"; label = f"◆ {score}"
        elif score >= 1:
            colour = "#6b7280"; label = f"· {score}"
        else:
            colour = "#d1d5db"; label = "·"
        return (
            f'<span style="background:{colour};color:#fff;'
            f'border-radius:4px;padding:1px 6px;font-size:11px;">{label}</span>'
        )

    rows = ""
    for company_name, items in sorted_companies:
        items_sorted = sorted(items, key=lambda x: x["score"], reverse=True)
        # Flag sweep results with a subtle indicator
        is_sweep = company_name.startswith("[Sweep]")
        label_style = "color:#7c3aed;" if is_sweep else "color:#111;"
        rows += (
            f'<tr><td colspan="2" style="padding:12px 8px 4px;'
            f'font-weight:bold;font-size:14px;{label_style}'
            f'border-top:2px solid #e5e7eb;">'
            f'{company_name}</td></tr>\n'
        )
        for item in items_sorted:
            title = item.get("title") or item["url"].split("/")[-1] or "(untitled)"
            rows += (
                f'<tr><td style="padding:3px 8px 3px 20px;font-size:13px;">'
                f'<a href="{item["url"]}" style="color:#1d4ed8;">{title}</a></td>'
                f'<td style="padding:3px 8px;white-space:nowrap;">'
                f'{score_badge(item["score"])}</td></tr>\n'
            )

    attention_section = ""
    if attention:
        shown = attention[:20]
        more = (f"<li style='font-size:12px;color:#92400e;'>...and {len(attention) - 20} more "
                f"(see company_health.json)</li>" if len(attention) > 20 else "")
        att = "".join(f"<li style='font-size:12px;color:#92400e;'>{a}</li>" for a in shown)
        attention_section = (
            f"<p style='margin-top:24px;color:#b45309;font-size:13px;font-weight:bold;'>"
            f"&#9888; Boards needing attention ({len(attention)})</p><ul>{att}{more}</ul>"
        )

    error_section = ""
    if errors:
        errs = "".join(f"<li style='font-size:12px;color:#6b7280;'>{e}</li>" for e in errors)
        error_section = (
            f"<p style='margin-top:24px;color:#9ca3af;font-size:12px;'>"
            f"⚠ Errors ({len(errors)}): <ul>{errs}</ul></p>"
        )

    summary_line = (
        f'<p style="color:#9ca3af;font-size:12px;margin-top:0;">{scrape_summary}</p>'
        if scrape_summary else ""
    )

    # Monday manual check section
    manual_section = ""
    if manual_check_companies and datetime.now(timezone.utc).weekday() == 0:
        mc_rows = "".join(
            f'<tr><td style="padding:4px 8px 4px 20px;font-size:13px;">'
            f'<a href="{co["url"]}" style="color:#1d4ed8;">{co["name"]}</a></td></tr>\n'
            for co in sorted(manual_check_companies, key=lambda c: c["name"].lower())
        )
        manual_section = f"""
<hr style="border:none;border-top:2px solid #e5e7eb;margin:24px 0 16px;">
<h3 style="color:#111;margin-bottom:4px;font-size:15px;">&#128269; Manual Check</h3>
<p style="color:#6b7280;font-size:12px;margin-top:0;">
  These {len(manual_check_companies)} companies can't be scraped automatically.
  Click each to check their careers page directly.
</p>
<table width="100%" cellpadding="0" cellspacing="0">
{mc_rows}
</table>"""

    html = f"""<!DOCTYPE html>
<html><body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:16px;">
<h2 style="color:#111;margin-bottom:4px;">Job Tracker Digest</h2>
<p style="color:#6b7280;font-size:13px;margin-top:0;">{run_time} &nbsp;&middot;&nbsp; {len(new_items)} new posting{"s" if len(new_items)!=1 else ""}</p>
{summary_line}
<p style="font-size:12px;color:#9ca3af;">
  Score legend:
  <span style="background:#1a7a3c;color:#fff;border-radius:4px;padding:1px 5px;">&#9733; 4+</span> strong match &nbsp;
  <span style="background:#2563eb;color:#fff;border-radius:4px;padding:1px 5px;">&#9670; 2-3</span> good match &nbsp;
  <span style="background:#6b7280;color:#fff;border-radius:4px;padding:1px 5px;">&middot; 1</span> weak match &nbsp;
  <span style="background:#d1d5db;color:#fff;border-radius:4px;padding:1px 5px;">&middot;</span> unscored
  &nbsp; <span style="color:#7c3aed;font-weight:bold;">Purple company name</span> = found via search sweep (not in watchlist)
</p>
<table width="100%" cellpadding="0" cellspacing="0">
{rows}
</table>
{attention_section}
{error_section}
{manual_section}
</body></html>"""
    return html


def send_email(subject: str, html_body: str, plain_body: str) -> None:
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    to_email = os.environ.get("TO_EMAIL")

    if not all([host, user, password, to_email]):
        log.warning("Email not configured (missing SMTP_HOST/SMTP_USER/SMTP_PASS/TO_EMAIL)")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_email
    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.sendmail(user, [to_email], msg.as_string())
        log.info(f"Email sent -> {to_email}")
    except Exception as e:
        log.error(f"Email send failed: {type(e).__name__}: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    log.info("JOB TRACKER STARTED")
    with open("companies.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    seen = load_seen()
    health = load_health()

    # Prune seen_jobs not sighted on any board for 90 days. Keyed on
    # last_seen_utc (falling back to first_seen for pre-migration entries):
    # pruning on first_seen resurrected still-live postings as "new" every
    # 90 days, re-emailing them and re-feeding the scoring pipeline.
    cutoff_dt = datetime.now(timezone.utc) - timedelta(days=90)
    pruned = {}
    for k, v in seen.items():
        last_seen = parse_dt(v.get("last_seen_utc") or v.get("first_seen_utc"))
        if not last_seen or last_seen >= cutoff_dt:
            pruned[k] = v
    if len(pruned) < len(seen):
        log.info(f"Pruned {len(seen) - len(pruned)} old entries from seen_jobs.json")
    seen = pruned

    new_items: list[dict] = []
    errors: list[str] = []
    companies_ok: int = 0
    companies_failed: int = 0

    # manual_check companies are skipped during scraping, shown in Monday digest.
    manual_check_companies = [c for c in config["companies"] if c.get("type") == "manual_check"]
    work = [c for c in config["companies"] if c.get("type") != "manual_check"]

    # Requests-based scrapers are I/O-bound and safe to run concurrently on the
    # shared thread-safe Session. (html_links is special-cased: it takes
    # defer_playwright so its slow Playwright escalation is batched into Pass 1b.)
    REQUEST_SCRAPERS = {
        "ashby_api": get_ashby_jobs,
        "greenhouse_api": get_greenhouse_jobs,
        "lever_api": get_lever_jobs,
        "workable_api": get_workable_jobs,
        "recruitee_api": get_recruitee_jobs,
        "bamboohr_api": get_bamboohr_jobs,
        "workday_api": get_workday_jobs,
        "rippling_api": get_rippling_jobs,
    }

    all_company_items: list[tuple[str, list[dict]]] = []
    playwright_queue: list[dict] = []

    def _scrape_requests(company: dict):
        name, ctype = company["name"], company["type"]
        if ctype == "playwright":
            return ("defer", company)
        if ctype != "html_links" and ctype not in REQUEST_SCRAPERS:
            log.warning(f"Unsupported type: {ctype} ({name})")
            return ("skip", name)
        try:
            if ctype == "html_links":
                items = get_html_links(company, defer_playwright=True)
            else:
                items = REQUEST_SCRAPERS[ctype](company)
            return ("ok", name, items)
        except _DeferToPlaywright:
            return ("defer", company)
        except Exception as e:
            return ("err", name, f"{type(e).__name__}: {e}")

    # ── Pass 1a: requests-based scrape, parallel (the 2+ hour runtime fix) ────
    log.info(f"Pass 1a: scraping {len(work)} companies with {MAX_SCRAPE_WORKERS} workers...")
    with ThreadPoolExecutor(max_workers=MAX_SCRAPE_WORKERS) as ex:
        for res in ex.map(_scrape_requests, work):
            if res[0] == "ok":
                all_company_items.append((res[1], res[2]))
                companies_ok += 1
                update_health(health, res[1], "ok", len(res[2]))
            elif res[0] == "defer":
                playwright_queue.append(res[1])
            elif res[0] == "err":
                log.error(f"{res[1]}: {res[2]}")
                errors.append(f"{res[1]}: {res[2]}")
                companies_failed += 1
                update_health(health, res[1], "err")
            # "skip": unsupported type, already warned

    # ── Pass 1b: Playwright for JS-heavy sites + escalations ─────────────────
    # Sequential by default: the Playwright sync API is not thread-safe. Bump
    # PLAYWRIGHT_WORKERS only behind a process pool.
    def _scrape_playwright(company: dict):
        name = company["name"]
        try:
            items = get_playwright_links(company)
            if company.get("link_contains"):
                needle = company["link_contains"]
                items = [i for i in items if needle in i.get("url", "")]
            return ("ok", name, items)
        except Exception as e:
            return ("err", name, f"{type(e).__name__}: {e}")

    if playwright_queue:
        log.info(f"Pass 1b: Playwright for {len(playwright_queue)} JS-heavy companies...")
        with ThreadPoolExecutor(max_workers=MAX_PLAYWRIGHT_WORKERS) as ex:
            for res in ex.map(_scrape_playwright, playwright_queue):
                if res[0] == "ok":
                    all_company_items.append((res[1], res[2]))
                    companies_ok += 1
                    update_health(health, res[1], "ok", len(res[2]))
                else:
                    log.error(f"{res[1]}: {res[2]}")
                    errors.append(f"{res[1]}: {res[2]}")
                    companies_failed += 1
                    update_health(health, res[1], "err")

    # Pass 2: identify all unseen items that need a title fetched.
    unseen_needing_title: list[dict] = []
    for name, items in all_company_items:
        for item in items:
            if (item["id"] not in seen and not item.get("title") and item.get("url")
                    and not is_junk_listing_url(item["url"])):
                unseen_needing_title.append(item)

    # Pass 3: fetch all missing titles concurrently in one batch.
    log.info(f"Fetching titles for {len(unseen_needing_title)} unseen items concurrently...")
    batch_fetch_titles(unseen_needing_title, max_workers=20)
    log.info("Title fetch complete.")

    # Pass 4: score, store, and build digest items.
    now_iso = datetime.now(timezone.utc).isoformat()
    for name, items in all_company_items:
        for item in items:
            item_id = item["id"]

            # Re-evaluate previously zero-scored items
            if item_id in seen:
                entry = seen[item_id]
                entry["last_seen_utc"] = now_iso
                if entry.get("scored") is False:
                    title = entry.get("title", "")
                    new_score = score_title(title, entry.get("url", ""))
                    if new_score > 0:
                        log.info(
                            f"  Re-scored previously zero-scored job: "
                            f"\'{title}\' now scores {new_score}"
                        )
                        entry["score"] = new_score
                        entry["scored"] = True
                        new_items.append({
                            "company": name,
                            "url": entry["url"],
                            "title": title,
                            "score": new_score,
                        })
                continue

            # Aggregator/browse URLs are never a single posting: suppress
            # permanently (stored in seen, score 0) so they neither leak into
            # the digest nor burn a title fetch on every future run.
            if is_junk_listing_url(item.get("url", "")):
                seen[item_id] = {
                    "company": name,
                    "url": item["url"],
                    "title": "",
                    "score": 0,
                    "scored": True,
                    "junk_url": True,
                    "first_seen_utc": datetime.now(timezone.utc).isoformat(),
                    "last_seen_utc": datetime.now(timezone.utc).isoformat(),
                }
                continue

            # New item -- title already populated by batch_fetch_titles above
            title = canonicalize_title(item.get("title") or "")

            if is_garbage_title(title):
                continue

            relevance = score_title(title, item.get("url", ""))

            seen[item_id] = {
                "company": name,
                "url": item["url"],
                "title": title,
                "score": relevance,
                "scored": relevance > 0,
                "first_seen_utc": datetime.now(timezone.utc).isoformat(),
                "last_seen_utc": datetime.now(timezone.utc).isoformat(),
            }

            if relevance > 0:
                new_items.append(
                    {"company": name, "url": item["url"], "title": title, "score": relevance}
                )


    # ── Weekly search sweep ───────────────────────────────────────────────
    sweep_items = run_weekly_search_sweep(config["companies"])
    for item in sweep_items:
        item_id = item["id"]
        if item_id not in seen:
            seen[item_id] = {
                "company": item["company"],
                "url": item["url"],
                "title": item.get("title", ""),
                "score": item["score"],
                "scored": True,
                "first_seen_utc": datetime.now(timezone.utc).isoformat(),
                "last_seen_utc": datetime.now(timezone.utc).isoformat(),
            }
            new_items.append(item)

    # ── Deduplicate same title across boards ─────────────────────────────
    new_items = deduplicate(new_items)

    save_seen(seen)
    save_health(health)
    attention = build_attention_list(health, {c["name"] for c in work})
    if attention:
        log.warning(f"{len(attention)} boards need attention:")
        for line in attention:
            log.warning(f"  {line}")

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_companies = companies_ok + companies_failed
    scrape_summary = f"{companies_ok}/{total_companies} companies scraped successfully"
    if companies_failed:
        scrape_summary += f" · {companies_failed} failed"

    log.info(scrape_summary)

    if new_items:
        subject = f"[Job Tracker] {len(new_items)} new posting{'s' if len(new_items)!=1 else ''} - {now_utc[:10]}"
        plain_lines = [
            f"Job Tracker Digest - {now_utc}",
            scrape_summary,
            f"{len(new_items)} new postings",
            "",
        ]
        for item in sorted(new_items, key=lambda x: x["score"], reverse=True):
            plain_lines.append(f"[{item['company']}] {item.get('title') or '(no title)'}")
            plain_lines.append(f"  {item['url']}")
        if attention:
            plain_lines += ["", f"Boards needing attention ({len(attention)}):"]
            plain_lines += [f"  {a}" for a in attention[:20]]
            if len(attention) > 20:
                plain_lines.append(f"  ...and {len(attention) - 20} more (see company_health.json)")
        plain_body = "\n".join(plain_lines)
    else:
        subject = f"No new jobs today - {now_utc[:10]}"
        plain_body = f"Job Tracker - {now_utc}\n{scrape_summary}\n\nNo new postings found."

    html_body = build_html_email(new_items, errors, now_utc, scrape_summary, manual_check_companies, attention)

    with open("latest_digest.html", "w", encoding="utf-8") as f:
        f.write(html_body)
    with open("latest_digest.txt", "w", encoding="utf-8") as f:
        f.write(plain_body)

    log.info("Sending email...")
    send_email(subject, html_body, plain_body)
    log.info("Done.")
    print(plain_body)


if __name__ == "__main__":
    main()
    
