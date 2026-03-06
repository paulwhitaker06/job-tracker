"""
job-tracker  –  check_jobs.py
Daily scraper: finds new job postings across 200 companies and emails a digest.

Improvements over v1
────────────────────
1. Smarter link filtering  – rejects nav/social/footer/image links much earlier
2. Pagination – follows "next page" links in HTML AND tries common URL patterns
3. JS-heavy sites – Workday, ADP, Rippling, BambooHR, etc. get Playwright fallback
4. Relevance scoring – every new posting is scored against a keyword list so the
   email is sorted with best-fit jobs at the top
5. HTML email  – clean, readable digest grouped by company with scores shown
6. Better error logging  – failures are collected and shown at the bottom of the email
7. LinkedIn URLs skipped gracefully with a warning instead of producing garbage
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urljoin, urldefrag, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

# ── logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger("job-tracker")

# ── constants ─────────────────────────────────────────────────────────────────
SEEN_FILE = "seen_jobs.json"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# ── relevance keywords ────────────────────────────────────────────────────────
# Edit this list to match your background.
# Higher weight = stronger signal.  Score ≥ 1 is shown; ≥ 3 is "strong match".
RELEVANCE_KEYWORDS: list[tuple[str, int]] = [
    # ── Seniority ──
    ("director", 3),
    ("VP", 3),
    ("vice president", 3),
    ("head of", 3),
    ("senior manager", 2),
    ("principal", 2),
    ("chief", 2),
    # ── Role types ──
    ("business development", 4),
    ("partnerships", 4),
    ("strategic partnerships", 5),
    ("commercialization", 4),
    ("commercial", 3),
    ("go-to-market", 4),
    ("GTM", 4),
    ("sales", 3),
    ("account executive", 3),
    ("account manager", 2),
    ("customer success", 2),
    ("solutions engineer", 2),
    ("product manager", 2),
    ("strategy", 3),
    ("licensing", 5),
    ("revenue", 2),
    ("alliances", 3),
    ("channel", 2),
    ("enterprise sales", 4),
    # ── Earth observation / satellite ──
    ("earth observation", 5),
    ("satellite imagery", 5),
    ("remote sensing", 5),
    ("SAR", 5),
    ("synthetic aperture radar", 5),
    ("optical imagery", 4),
    ("multispectral", 4),
    ("hyperspectral", 4),
    ("LiDAR", 3),
    ("radar", 3),
    ("AIS", 5),
    ("RF", 4),
    ("radio frequency", 4),
    ("geospatial", 4),
    ("GIS", 3),
    ("satellite data", 5),
    ("space data", 3),
    ("aerial imagery", 3),
    # ── Maritime / fishing (GFW specialty) ──
    ("maritime", 5),
    ("vessel", 4),
    ("shipping", 3),
    ("AIS data", 5),
    ("fishing", 4),
    ("IUU", 5),
    ("illegal fishing", 5),
    ("ocean", 3),
    ("marine", 3),
    ("port", 2),
    ("dark vessel", 4),
    ("vessel monitoring", 5),
    ("dark shipping", 4),
    # ── Environmental / climate ──
    ("environmental monitoring", 5),
    ("climate", 3),
    ("carbon", 3),
    ("emissions", 3),
    ("sustainability", 2),
    ("ESG", 3),
    ("deforestation", 4),
    ("forest monitoring", 5),
    ("biodiversity", 3),
    ("nature-based", 3),
    ("oil spill", 5),
    ("methane", 4),
    ("GHG", 3),
    ("greenhouse gas", 3),
    ("flood", 3),
    ("wildfire", 3),
    # ── Supply chain / risk / insurance ──
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
    # ── Government / defense ──
    ("government", 2),
    ("defense", 2),
    ("intelligence", 2),
    ("national security", 3),
    # ── Agriculture / land ──
    ("agriculture", 3),
    ("agri", 2),
    ("crop", 2),
    ("food security", 3),
    ("forestry", 3),
    # ── Data / tech ──
    ("API", 2),
    ("data platform", 2),
    ("analytics", 2),
    ("data licensing", 5),
    ("data products", 3),
]


def score_title(title: str) -> int:
    """Return a relevance score for a job title / URL string."""
    text = title.lower()
    return sum(w for kw, w in RELEVANCE_KEYWORDS if kw.lower() in text)


# ── utilities ─────────────────────────────────────────────────────────────────

def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def load_seen() -> dict:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_seen(seen: dict) -> None:
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, indent=2, sort_keys=True)


def fetch_html(url: str, timeout: int = 45) -> str:
    r = requests.get(url, timeout=timeout, headers=HEADERS)
    r.raise_for_status()
    return r.text


# ── link extraction ───────────────────────────────────────────────────────────

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
    "/o/",          # recruitee
    "/j/",          # various ATS
    # ATS hosts
    "jobs.lever.co/",
    "jobs.ashbyhq.com/",
    "greenhouse.io/",
    "job-boards.greenhouse.io/",
    "job-boards.eu.greenhouse.io/",
    "boards.greenhouse.io/",
    "apply.workable.com/",
    "applytojob.com/apply/",
    "bamboohr.com/careers",
    "myworkdayjobs.com/",
    "recruitee.com/o/",
    "personio.de/job/",
    "personio.com/job/",
    "factorial.it/",
    "hrmos.co/",
    "smartrecruiters.com/",
    "icims.com/",
    "teamtailor.com/",
    "careers.team/",
    "pinpointhq.com/",
    "rippling.com/",
    "breezy.hr/",
    "gohire.io/",
    "gusto.com/boards/",
    "paylocity.com/recruiting/",
    "hibob.com/jobs",
    "zohorecruit.com/jobs/",
    "comeet.com/jobs/",
]

# These ATS hosts are "board" pages – safe to follow one level deeper
BOARD_HOSTS = [
    "jobs.lever.co/", "jobs.ashbyhq.com/", "apply.workable.com/",
    "job-boards.eu.greenhouse.io/", "job-boards.greenhouse.io/",
    "boards.greenhouse.io/", "greenhouse.io/",
    "bamboohr.com/careers", "myworkdayjobs.com/",
    "personio.de/", "personio.com/", "recruitee.com/",
    "factorial.it/", "hrmos.co/", "smartrecruiters.com/",
    "icims.com/", "teamtailor.com/", "applytojob.com/",
    "careers.team/", "pinpointhq.com/", "breezy.hr/",
    "gohire.io/", "gusto.com/boards/", "paylocity.com/recruiting/",
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

        # Lever filter pages (not real postings)
        if "jobs.lever.co/" in u and "?" in u:
            path = u.split("jobs.lever.co/", 1)[1]
            if path.count("/") < 1:
                continue

        if any(ind in u for ind in JOB_INDICATORS):
            links.add(full)

    return links


def find_next_page_links(html: str, base_url: str) -> set[str]:
    """
    Follow explicit 'Next' / 'Load more' / page-number links in HTML.
    Returns absolute URLs of candidate next pages.
    """
    soup = BeautifulSoup(html, "html.parser")
    candidates: set[str] = set()
    next_patterns = re.compile(
        r"\bnext\b|\bnext\s*page\b|load\s*more|show\s*more|»|›|page\s*\d",
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
    """Generate common pagination URL guesses."""
    sep = "&" if "?" in base_url else "?"
    b = base_url.rstrip("/")
    return [
        f"{base_url}{sep}page=2",
        f"{base_url}{sep}page=3",
        f"{base_url}{sep}paged=2",
        f"{base_url}{sep}paged=3",
        f"{base_url}{sep}offset=20",
        f"{base_url}{sep}offset=40",
        f"{b}/page/2",
        f"{b}/page/3",
        f"{b}/jobs",
        f"{b}/jobs?page=2",
        f"{b}/careers?page=2",
    ]


def is_board_url(url: str) -> bool:
    u = url.lower()
    return any(b in u for b in BOARD_HOSTS)


# ── JS-heavy site detection ───────────────────────────────────────────────────

JS_HEAVY_PATTERNS = [
    "myworkdayjobs.com", "wd1.myworkdaysite.com", "wd3.myworkdaysite.com",
    "wd5.myworkdayjobs.com", "workforcenow.adp.com",
    "ats.rippling.com",
]


def is_js_heavy(url: str) -> bool:
    u = url.lower()
    return any(p in u for p in JS_HEAVY_PATTERNS)


# ── per-type scrapers ─────────────────────────────────────────────────────────

def get_html_links(company: dict) -> list[dict]:
    """
    HTML harvesting with:
    - common pagination URL guesses
    - 'Next page' link following (up to 5 extra pages)
    - depth-1 follow for outbound ATS board links
    - Playwright fallback for JS-heavy sites
    """
    base_url = company["url"]

    # Skip LinkedIn – can't scrape without auth
    if "linkedin.com" in base_url.lower():
        log.warning(f"  {company['name']}: LinkedIn URL – skipping (requires login)")
        return []

    # Playwright fallback for JS-heavy sites
    if is_js_heavy(base_url):
        log.info(f"  {company['name']}: JS-heavy site, using Playwright")
        return get_playwright_links(company)

    pages_to_fetch: set[str] = {base_url}
    pages_to_fetch.update(pagination_urls(base_url))

    links: set[str] = set()
    fetched: set[str] = set()

    for page_url in sorted(pages_to_fetch):
        try:
            html = fetch_html(page_url)
            fetched.add(page_url)
            new_links = extract_links(html, page_url)
            links |= new_links

            # Follow explicit next-page links (up to 5 extra pages)
            if page_url == base_url:
                for np in find_next_page_links(html, page_url):
                    if np not in fetched and len(fetched) < 8:
                        try:
                            np_html = fetch_html(np)
                            links |= extract_links(np_html, np)
                            fetched.add(np)
                        except Exception:
                            pass
        except Exception:
            pass

    # Depth-1 follow into ATS board pages
    board_links = sorted({l for l in links if is_board_url(l) and l != base_url})
    for board_url in board_links[:3]:
        try:
            board_html = fetch_html(board_url)
            links |= extract_links(board_html, board_url)
        except Exception:
            pass

    # Optional containment filter
    if company.get("link_contains"):
        needle = company["link_contains"]
        links = {l for l in links if needle in l}

    return [
        {"id": sha(company["name"] + "|" + l), "url": l, "title": None}
        for l in sorted(links)
    ]


def get_playwright_links(company: dict) -> list[dict]:
    """
    Use Playwright to render a JS-heavy careers page and extract links.
    Falls back to a page-hash change sentinel if link extraction yields nothing.
    """
    try:
        from playwright.sync_api import sync_playwright

        url = company["url"]
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=120_000)

            # Try scrolling to trigger lazy-load
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

            html = page.content()
            browser.close()

        links = extract_links(html, url)

        if links:
            return [
                {"id": sha(company["name"] + "|" + l), "url": l, "title": None}
                for l in sorted(links)
            ]
        else:
            # Fall back to page-hash change detection
            text = BeautifulSoup(html, "html.parser").get_text()
            content_hash = sha(text)
            return [
                {
                    "id": sha(company["name"] + "|pagehash|" + content_hash),
                    "url": url,
                    "title": "Careers page changed (JS site – visit to see jobs)",
                }
            ]
    except ImportError:
        log.warning("Playwright not installed – skipping JS site: " + company["name"])
        return []
    except Exception as e:
        log.warning(f"Playwright failed for {company['name']}: {e}")
        return []


def get_greenhouse_jobs(company: dict) -> list[dict]:
    board = company.get("board")
    url = company.get("url", "")
    if board:
        gh_url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    elif "boards-api.greenhouse.io" in url:
        gh_url = url
    else:
        raise ValueError("Greenhouse: missing 'board' key")

    r = requests.get(gh_url, timeout=45, headers=HEADERS)
    r.raise_for_status()
    data = r.json()

    results = []
    for job in data.get("jobs", []):
        job_url = job.get("absolute_url") or job.get("url")
        title = job.get("title") or ""
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
    r = requests.get(api_url, timeout=45, headers=HEADERS)
    r.raise_for_status()
    data = r.json()

    results = []
    for job in data:
        job_url = job.get("hostedUrl") or job.get("applyUrl")
        title = job.get("text") or job.get("title") or ""
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

    api_url = f"https://apply.workable.com/api/v3/accounts/{account}/jobs?state=published"
    try:
        r = requests.get(api_url, timeout=45, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        results = []
        for job in data.get("results", []):
            job_url = job.get("shortlink") or job.get("url")
            title = job.get("title") or ""
            job_id = job.get("id") or sha(job_url or title)
            if not job_url:
                continue
            results.append(
                {"id": sha(company["name"] + "|" + str(job_id)), "url": job_url, "title": title}
            )
        return results
    except Exception:
        board_url = f"https://apply.workable.com/{account}/"
        html = fetch_html(board_url)
        links = {l for l in extract_links(html, board_url) if "apply.workable.com" in l}
        return [
            {"id": sha(company["name"] + "|" + l), "url": l, "title": None}
            for l in sorted(links)
        ]


def get_ashby_jobs(company: dict) -> list[dict]:
    r = requests.get(company["url"], timeout=45, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    results = []
    for job in data.get("jobs", []):
        job_url = job.get("jobUrl")
        if not job_url:
            continue
        job_id = job.get("id") or sha(job_url)
        results.append(
            {
                "id": sha(company["name"] + "|" + str(job_id)),
                "url": job_url,
                "title": job.get("title"),
            }
        )
    return results


def fetch_title(url: str) -> str:
    try:
        r = requests.get(url, timeout=20, headers=HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Try <title> first, then og:title, then h1
        if soup.title and soup.title.string:
            t = soup.title.string.strip()
            # Strip common boilerplate suffixes
            for sep in [" - ", " | ", " – ", " — ", " at ", " :: "]:
                if sep in t:
                    t = t.split(sep)[0].strip()
            return t
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og["content"].strip()
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)
    except Exception:
        pass
    return ""


# ── email ─────────────────────────────────────────────────────────────────────

def build_html_email(new_items: list[dict], errors: list[str], run_time: str) -> str:
    """Build a clean HTML email sorted by relevance score."""

    # Group by company, sorted within each company by score
    from collections import defaultdict
    by_company: dict[str, list[dict]] = defaultdict(list)
    for item in new_items:
        by_company[item["company"]].append(item)

    # Sort companies by their best score (descending)
    sorted_companies = sorted(
        by_company.items(),
        key=lambda kv: max(i["score"] for i in kv[1]),
        reverse=True,
    )

    # Score colour helper
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
        rows += (
            f'<tr><td colspan="2" style="padding:12px 8px 4px;'
            f'font-weight:bold;font-size:14px;color:#111;'
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

    error_section = ""
    if errors:
        errs = "".join(f"<li style='font-size:12px;color:#6b7280;'>{e}</li>" for e in errors)
        error_section = f"<p style='margin-top:24px;color:#9ca3af;font-size:12px;'>⚠ Errors ({len(errors)}): <ul>{errs}</ul></p>"

    html = f"""<!DOCTYPE html>
<html><body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:16px;">
<h2 style="color:#111;margin-bottom:4px;">Job Tracker Digest</h2>
<p style="color:#6b7280;font-size:13px;margin-top:0;">{run_time} &nbsp;·&nbsp; {len(new_items)} new posting{"s" if len(new_items)!=1 else ""}</p>
<p style="font-size:12px;color:#9ca3af;">
  Score legend: <span style="background:#1a7a3c;color:#fff;border-radius:4px;padding:1px 5px;">★ 4+</span> strong match &nbsp;
  <span style="background:#2563eb;color:#fff;border-radius:4px;padding:1px 5px;">◆ 2-3</span> good match &nbsp;
  <span style="background:#6b7280;color:#fff;border-radius:4px;padding:1px 5px;">· 1</span> weak match &nbsp;
  <span style="background:#d1d5db;color:#fff;border-radius:4px;padding:1px 5px;">·</span> unscored
</p>
<table width="100%" cellpadding="0" cellspacing="0">
{rows}
</table>
{error_section}
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
        log.info(f"Email sent → {to_email}")
    except Exception as e:
        log.error(f"Email send failed: {type(e).__name__}: {e}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    log.info("JOB TRACKER STARTED")
    with open("companies.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    seen = load_seen()
    new_items: list[dict] = []
    errors: list[str] = []

    for company in config["companies"]:
        name = company["name"]
        ctype = company["type"]
        log.info(f"Checking {name} ({ctype})")

        try:
            if ctype == "html_links":
                items = get_html_links(company)
            elif ctype == "ashby_api":
                items = get_ashby_jobs(company)
            elif ctype == "playwright":
                items = get_playwright_links(company)
            elif ctype == "greenhouse_api":
                items = get_greenhouse_jobs(company)
            elif ctype == "lever_api":
                items = get_lever_jobs(company)
            elif ctype == "workable_api":
                items = get_workable_jobs(company)
            else:
                log.warning(f"Unsupported type: {ctype}")
                continue

            for item in items:
                item_id = item["id"]
                if item_id not in seen:
                    title = item.get("title") or ""
                    if not title and item.get("url"):
                        title = fetch_title(item["url"])

                    relevance = score_title(title + " " + item.get("url", ""))

                    seen[item_id] = {
                        "company": name,
                        "url": item["url"],
                        "title": title,
                        "score": relevance,
                        "first_seen_utc": datetime.now(timezone.utc).isoformat(),
                    }
                    new_items.append(
                        {"company": name, "url": item["url"], "title": title, "score": relevance}
                    )

        except Exception as e:
            msg = f"{name}: {type(e).__name__}: {e}"
            log.error(msg)
            errors.append(msg)

    save_seen(seen)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if new_items:
        subject = f"🛰 {len(new_items)} new job posting{'s' if len(new_items)!=1 else ''} – {now_utc[:10]}"
        # Plain-text fallback
        plain_lines = [f"Job Tracker Digest – {now_utc}", f"{len(new_items)} new postings", ""]
        for item in sorted(new_items, key=lambda x: x["score"], reverse=True):
            plain_lines.append(f"[{item['company']}] {item.get('title') or '(no title)'}")
            plain_lines.append(f"  {item['url']}")
        plain_body = "\n".join(plain_lines)
    else:
        subject = f"No new jobs today – {now_utc[:10]}"
        plain_body = f"Job Tracker – {now_utc}\n\nNo new postings found."

    html_body = build_html_email(new_items, errors, now_utc)

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
