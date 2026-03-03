import os
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
from urllib.parse import urljoin, urldefrag

import requests
import yaml
from bs4 import BeautifulSoup

SEEN_FILE = "seen_jobs.json"


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


def fetch_html(url: str) -> str:
    r = requests.get(url, timeout=45, headers={"User-Agent": "job-tracker/1.0"})
    r.raise_for_status()
    return r.text


def extract_links_from_html(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href:
            continue

        # Drop pure anchors and JS pseudo-links
        if href == "#" or href.startswith("javascript:"):
            continue

        # Resolve relative to absolute
        abs_url = urljoin(base_url, href)

        # Remove fragment so we do not treat same page section links as unique jobs
        abs_url, _frag = urldefrag(abs_url)

        links.add(abs_url)

    return links


def get_html_links(company: dict) -> list[dict]:
    html = fetch_html(company["url"])
    links = extract_links_from_html(html, company["url"])

    if company.get("link_contains"):
        needle = company["link_contains"]
        links = {l for l in links if needle in l}

    results = []
    for link in sorted(links):
        results.append(
            {
                "id": sha(company["name"] + "|" + link),
                "url": link,
                "title": None,
            }
        )
    return results


def get_ashby_jobs(company: dict) -> list[dict]:
    r = requests.get(company["url"], timeout=45, headers={"User-Agent": "job-tracker/1.0"})
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


def get_playwright_page_change(company: dict) -> list[dict]:
    from playwright.sync_api import sync_playwright

    url = company["url"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=120000)
        text = page.inner_text("body")
        browser.close()

    content_hash = sha(text)

    return [
        {
            "id": sha(company["name"] + "|pagehash|" + content_hash),
            "url": url,
            "title": "Careers page changed (JS site)",
        }
    ]
def fetch_title(url: str) -> str:
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "job-tracker/1.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        if soup.title and soup.title.string:
            return soup.title.string.strip()

    except Exception:
        pass

    return ""

def send_email(subject: str, body: str) -> None:
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    to_email = os.environ.get("TO_EMAIL")

    if not all([host, user, password, to_email]):
        print("Email not configured. Missing SMTP_HOST/SMTP_USER/SMTP_PASS/TO_EMAIL.")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_email

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to_email], msg.as_string())

def main():
    print("JOB TRACKER STARTED")
    with open("companies.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    seen = load_seen()
    new_items: list[dict] = []

    for company in config["companies"]:
        name = company["name"]
        ctype = company["type"]
        print(f"Checking {name} ({ctype})")

        try:
            if ctype == "html_links":
                items = get_html_links(company)
            elif ctype == "ashby_api":
                items = get_ashby_jobs(company)
            elif ctype == "playwright":
                items = get_playwright_page_change(company)
            else:
                print(f"Skipping unsupported type: {ctype}")
                continue

            for item in items:
                item_id = item["id"]

                if item_id not in seen:
                    title = item.get("title") or ""

                    if not title and item.get("url"):
                        title = fetch_title(item["url"])

                    seen[item_id] = {
                        "company": name,
                        "url": item["url"],
                        "title": title,
                        "first_seen_utc": datetime.now(timezone.utc).isoformat(),
                    }

                    new_items.append(
                        {
                            "company": name,
                            "url": item["url"],
                            "title": title,
                        }
                    )

        except Exception as e:
            print(f"Error with {name}: {e}")

    save_seen(seen)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append("Daily job tracker digest")
    lines.append(f"Run time: {now_utc}")
    lines.append("")

    if new_items:
        lines.append(f"New items: {len(new_items)}")
        lines.append("")
        for item in new_items:
            title = item.get("title") or "(no title captured)"
            lines.append(f"- {item['company']}: {title}")
            lines.append(f"  {item['url']}")
        subject = f"New jobs detected: {len(new_items)}"
    else:
        lines.append("No new items today.")
        subject = "No new jobs today"

    body = "\n".join(lines)

    with open("latest_digest.txt", "w", encoding="utf-8") as f:
        f.write(body)

    send_email(subject, body)

    print(body)
