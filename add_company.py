#!/usr/bin/env python3
"""
add_company.py — add a single verified company to companies.yaml

Usage:
  python3 add_company.py "Company Name" "https://careers.url"
  python3 add_company.py "Company Name" "https://careers.url" playwright
  python3 add_company.py "Company Name" "https://jobs.lever.co/slug" lever_api
  python3 add_company.py "Company Name" "https://job-boards.greenhouse.io/slug" greenhouse_api

Safety checks:
  - Fetches the URL first to confirm it returns 200 with job-related content.
  - Rejects 404s and connection errors.
  - Skips duplicates (same name or same URL already in yaml).
  - Validates YAML is parseable after write.

Type defaults to html_links if not specified. Valid types:
  html_links, playwright, lever_api, greenhouse_api, workable_api, ashby_api, manual_check

For api types, required fields are auto-inferred from URL when possible:
  - lever_api: infers lever_company from jobs.lever.co/{slug}
  - greenhouse_api: infers board from /{slug} at the end of URL
  - workable_api: infers workable_account from apply.workable.com/{account}
"""

import re
import sys
import yaml
import requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

VALID_TYPES = {"html_links", "playwright", "lever_api", "greenhouse_api",
               "workable_api", "ashby_api", "manual_check"}

JOB_TEXT = re.compile(
    r"\b(job|jobs|career|careers|opening|openings|position|positions|"
    r"vacancy|vacancies|role|roles|apply|hiring)\b", re.I)


def verify_url(url, ctype):
    """Fetch URL and confirm it's live. For API types, skip keyword check."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.ConnectionError:
        return False, "connection error"
    except Exception as e:
        return False, f"{type(e).__name__}"

    if r.status_code == 404:
        return False, "404 not found"
    if r.status_code >= 400:
        return False, f"HTTP {r.status_code}"

    # For html_links and playwright, check the page actually mentions jobs
    if ctype in {"html_links", "playwright"}:
        if not JOB_TEXT.search(r.text or ""):
            return False, "page does not contain job-related keywords"

    return True, f"OK (HTTP {r.status_code})"


def infer_api_fields(url, ctype):
    """Return dict of API-specific fields inferred from URL."""
    fields = {}
    u = url.lower()
    if ctype == "lever_api" and "jobs.lever.co/" in u:
        slug = u.split("jobs.lever.co/", 1)[1].split("/", 1)[0].rstrip("/")
        if slug:
            fields["lever_company"] = slug
    elif ctype == "greenhouse_api":
        # URL pattern: job-boards.greenhouse.io/{board} or boards.greenhouse.io/{board}
        m = re.search(r"greenhouse\.io/([a-z0-9_-]+)", u)
        if m:
            fields["board"] = m.group(1)
    elif ctype == "workable_api" and "apply.workable.com/" in u:
        acct = u.split("apply.workable.com/", 1)[1].split("/", 1)[0].rstrip("/")
        if acct:
            fields["workable_account"] = acct
    return fields


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 add_company.py \"Company Name\" \"https://url\" [type]")
        print("Types: html_links (default), playwright, lever_api, greenhouse_api, workable_api, ashby_api, manual_check")
        sys.exit(1)

    name = sys.argv[1].strip()
    url = sys.argv[2].strip().rstrip("/")
    ctype = sys.argv[3].strip() if len(sys.argv) >= 4 else "html_links"

    if not name:
        print("ERROR: name is empty")
        sys.exit(1)
    if not url.startswith("http"):
        print(f"ERROR: URL must start with http:// or https:// (got: {url})")
        sys.exit(1)
    if ctype not in VALID_TYPES:
        print(f"ERROR: invalid type '{ctype}'. Valid: {sorted(VALID_TYPES)}")
        sys.exit(1)

    # Load yaml
    with open("companies.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Dedup check
    existing_names = {c["name"].lower() for c in config["companies"]}
    existing_urls = {c["url"].lower().rstrip("/") for c in config["companies"]}

    if name.lower() in existing_names:
        print(f"SKIP: '{name}' already in companies.yaml")
        sys.exit(0)
    if url.lower() in existing_urls:
        # Find the existing entry
        match = next(c["name"] for c in config["companies"]
                     if c["url"].lower().rstrip("/") == url.lower())
        print(f"SKIP: URL already in companies.yaml under name '{match}'")
        sys.exit(0)

    # Verify URL (skip for manual_check)
    if ctype != "manual_check":
        print(f"Verifying {url} ...")
        ok, detail = verify_url(url, ctype)
        if not ok:
            print(f"FAIL: {detail}")
            print(f"\nWill not add. Fix the URL and try again, or use 'manual_check' as the type:")
            print(f'  python3 add_company.py "{name}" "{url}" manual_check')
            sys.exit(1)
        print(f"OK: {detail}")

    # Build entry
    entry = {"name": name, "type": ctype, "url": url}
    entry.update(infer_api_fields(url, ctype))

    # Validate API entries have required fields
    if ctype == "greenhouse_api" and "board" not in entry:
        print(f"ERROR: greenhouse_api requires 'board' but couldn't infer from URL.")
        print(f"  URL must end with /{{board-slug}} e.g. https://job-boards.greenhouse.io/slug")
        sys.exit(1)
    if ctype == "lever_api" and "lever_company" not in entry:
        print(f"ERROR: lever_api requires URL to contain jobs.lever.co/{{slug}}")
        sys.exit(1)
    if ctype == "workable_api" and "workable_account" not in entry:
        print(f"ERROR: workable_api requires URL to contain apply.workable.com/{{account}}")
        sys.exit(1)

    # Append and rewrite
    config["companies"].append(entry)
    lines = ["companies:"]
    for c in config["companies"]:
        lines.append(f"  - name: {c['name']}")
        lines.append(f"    type: {c['type']}")
        lines.append(f"    url: {c['url']}")
        if "link_contains" in c:
            lines.append(f"    link_contains: {c['link_contains']}")
        if "board" in c:
            lines.append(f"    board: {c['board']}")
        if "workable_account" in c:
            lines.append(f"    workable_account: {c['workable_account']}")
        if "lever_company" in c:
            lines.append(f"    lever_company: {c['lever_company']}")
        lines.append("")
    with open("companies.yaml", "w") as f:
        f.write("\n".join(lines))

    # Validate result parses cleanly
    with open("companies.yaml", "r") as f:
        check = yaml.safe_load(f)

    print(f"\nADDED: {name}")
    print(f"  type: {ctype}")
    print(f"  url:  {url}")
    for k, v in entry.items():
        if k not in {"name", "type", "url"}:
            print(f"  {k}: {v}")
    print(f"\nTotal companies: {len(check['companies'])}")


if __name__ == "__main__":
    main()
