#!/usr/bin/env python3
"""
verify_and_add_candidates.py

Runs on Paul's Mac (where it has real network access) to verify candidate
career page URLs before adding them to companies.yaml.

For each candidate:
  1. Fetches the URL with a real HTTP request.
  2. Checks for 200 status.
  3. Checks that the page contains evidence of being a real careers page
     (keywords like "job", "career", "position", "opening", "apply").
  4. Checks that the page contains at least one <a> link that looks like a
     job posting (using the same patterns as check_jobs.py).

Only candidates passing ALL checks are added to companies.yaml.

Usage:
  python3 verify_and_add_candidates.py

Output:
  - Prints each candidate with PASS/FAIL/WEAK status.
  - Writes verified entries to companies.yaml.
  - Writes rejected entries to rejected_candidates.txt with the reason.
"""

import re
import sys
import yaml
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Same job indicators used in check_jobs.py
JOB_INDICATORS = [
    "/apply/", "/jobs/", "/job/", "/positions/", "/openings/",
    "/vacancies/", "/careers/", "/career/", "/opportunities/",
    "/role/", "/roles/", "/posting/", "/postings/",
    "/recruitment/", "/jobdetail/", "/job-details/",
    "jobs.lever.co/", "jobs.ashbyhq.com/", "greenhouse.io/",
    "job-boards.greenhouse.io/", "apply.workable.com/",
    "bamboohr.com/careers", "personio.de/job/", "recruitee.com/o/",
    "teamtailor.com/", "breezy.hr/", "gohire.io/", "gusto.com/boards/",
    "myworkdayjobs.com/", "icims.com/", "smartrecruiters.com/",
    "applytojob.com/", "rippling.com/", "paylocity.com/recruiting/",
    "hibob.com/jobs", "zohorecruit.com/",
]

JOB_TEXT = re.compile(r"\b(job|jobs|career|careers|opening|openings|position|positions|vacancy|vacancies|role|roles|apply|hiring)\b", re.I)

# ─────────────────────────────────────────────────────────────────────────
# CANDIDATE POOL
# Companies / URLs to verify. ONLY entries that pass verification get added.
# Organized by category for readability.
# ─────────────────────────────────────────────────────────────────────────
CANDIDATES = [
    # Weather / atmospheric intelligence
    ("Meteomatics", "https://www.meteomatics.com/en/careers/"),
    ("WeatherXM", "https://weatherxm.com/careers/"),
    ("Vaisala", "https://www.vaisala.com/en/careers"),
    ("Salient Predictions", "https://salientpredictions.com/careers/"),
    ("AER Atmospheric Research", "https://www.aer.com/careers/"),

    # Water tech / aquaculture
    ("Ketos", "https://ketos.co/careers/"),
    ("Aquabyte", "https://aquabyte.ai/careers/"),
    ("Tule Technologies", "https://tuletechnologies.com/careers/"),
    ("Kilimo", "https://kilimo.com/careers/"),
    ("Ceres Imaging", "https://www.ceresimaging.net/careers/"),
    ("FIDO Tech", "https://www.fido.tech/careers/"),

    # Forest / biodiversity monitoring
    ("Rainforest Connection", "https://rfcx.org/careers"),
    ("NatureServe", "https://www.natureserve.org/careers"),
    ("Biome Makers", "https://biomemakers.com/careers"),
    ("Forest Trends", "https://www.forest-trends.org/careers/"),
    ("CGIAR", "https://www.cgiar.org/careers/"),

    # Agtech / precision ag
    ("Cropin", "https://www.cropin.com/careers"),
    ("Indigo Ag", "https://www.indigoag.com/careers"),
    ("Farmers Business Network", "https://www.fbn.com/careers"),
    ("Semios", "https://semios.com/careers/"),
    ("CropX", "https://cropx.com/careers/"),
    ("Greeneye Technology", "https://www.greeneye.technology/careers/"),
    ("Carbon Robotics", "https://carbonrobotics.com/careers"),
    ("AgriWebb", "https://www.agriwebb.com/careers/"),
    ("Hortau", "https://hortau.com/careers/"),
    ("BeeHero", "https://beehero.io/careers/"),

    # Air quality / emissions
    ("Aclima", "https://aclima.io/careers/"),
    ("Kairos Aerospace", "https://kairosaerospace.com/careers/"),
    ("SeekOps", "https://www.seekops.com/careers"),
    ("LongPath Technologies", "https://www.longpathtech.com/careers"),
    ("Project Canary", "https://www.projectcanary.com/careers/"),
    ("Bridger Photonics", "https://www.bridgerphotonics.com/careers"),

    # Carbon removal / CDR
    ("Climeworks", "https://climeworks.com/careers"),
    ("Carbon Engineering", "https://carbonengineering.com/careers/"),
    ("Vesta", "https://www.vesta.earth/careers"),
    ("Running Tide", "https://www.runningtide.com/careers"),
    ("Captura", "https://capturacorp.com/careers"),
    ("Ebb Carbon", "https://www.ebbcarbon.com/careers"),
    ("Equatic", "https://www.equatic.tech/careers"),
    ("Verdox", "https://verdox.com/careers/"),
    ("Noya", "https://www.noya.co/careers"),
    ("Spiritus", "https://spiritus.earth/careers"),
    ("Holocene", "https://www.holocene.company/careers"),
    ("Travertine", "https://travertinetech.com/careers"),
    ("Mati Carbon", "https://www.mati.earth/careers"),

    # Maritime / blue economy
    ("Seabound", "https://www.seabound.co/careers"),
    ("Amogy", "https://amogy.co/careers/"),
    ("Fleetzero", "https://fleetzero.com/careers"),
    ("ZeroNorth", "https://zeronorth.com/careers/"),
    ("Nautilus Labs", "https://nautiluslabs.com/careers/"),

    # Geospatial SaaS
    ("Pix4D", "https://www.pix4d.com/careers"),
    ("Foursquare", "https://careers.foursquare.com/"),
    ("Placer.ai", "https://www.placer.ai/careers"),
    ("SafeGraph", "https://www.safegraph.com/careers"),
    ("Cape Analytics", "https://capeanalytics.com/careers/"),

    # Climate VC portfolio boards (Getro pattern - common but need to verify)
    ("Elemental Excelerator Portfolio", "https://jobs.elementalexcelerator.com/jobs"),
    ("MCJ Collective Portfolio", "https://jobs.mcjcollective.com/jobs"),
    ("World Fund Portfolio", "https://jobs.worldfund.vc/jobs"),
    ("2150 VC Portfolio", "https://jobs.2150.vc/jobs"),
    ("At One Ventures Portfolio", "https://jobs.atoneventures.com/jobs"),
    ("Systemiq Capital Portfolio", "https://jobs.systemiq.earth/jobs"),
    ("Voyager Ventures Portfolio", "https://jobs.voyagervc.com/jobs"),
    ("SOSV Portfolio", "https://jobs.sosv.com/jobs"),
    ("Third Sphere Portfolio", "https://jobs.thirdsphere.com/jobs"),

    # Federal / intel commercial
    ("L3Harris", "https://careers.l3harris.com/"),
    ("Leidos", "https://careers.leidos.com/"),
    ("CACI", "https://careers.caci.com/"),
    ("SAIC", "https://jobs.saic.com/"),
    ("Booz Allen", "https://www.boozallen.com/careers/"),
    ("BlueHalo", "https://www.bluehalo.com/careers/"),

    # NGOs / foundations
    ("Blue Ventures", "https://blueventures.org/careers/"),
    ("Bezos Earth Fund", "https://www.bezosearthfund.org/careers"),
    ("Moore Foundation", "https://www.moore.org/careers"),
    ("Hewlett Foundation", "https://hewlett.org/about-us/careers/"),
    ("MacArthur Foundation", "https://www.macfound.org/about/careers"),
    ("Packard Foundation", "https://www.packard.org/about-the-foundation/careers/"),
    ("Allen Institute for AI", "https://allenai.org/careers"),
    ("Coral Reef Alliance", "https://coral.org/careers/"),
    ("IUCN", "https://www.iucn.org/about-iucn/jobs"),
    ("UNEP", "https://www.unep.org/jobs"),
    ("NOAA", "https://www.noaa.gov/careers"),
    ("USGS", "https://www.usgs.gov/about/careers"),
    ("Stockholm Environment Institute", "https://www.sei.org/about-sei/vacancies/"),

    # Additional Weather / data
    ("Understory", "https://understoryweather.com/careers/"),

    # Additional maritime
    ("Shone", "https://www.shone.ai/careers"),

    # Alternative URL patterns worth trying for some names
    ("Climeworks (alt)", "https://climeworks.com/jobs"),
    ("Carbon Engineering (alt)", "https://carbonengineering.com/jobs"),
]

def verify(name, url):
    """Try to fetch url. Return (name, url, status, detail)."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
    except requests.exceptions.Timeout:
        return name, url, "FAIL", "timeout"
    except requests.exceptions.ConnectionError as e:
        return name, url, "FAIL", f"connection error"
    except Exception as e:
        return name, url, "FAIL", f"{type(e).__name__}"

    if r.status_code == 404:
        return name, url, "FAIL", "404 not found"
    if r.status_code >= 400:
        return name, url, "FAIL", f"HTTP {r.status_code}"
    if r.status_code >= 300:
        return name, url, "FAIL", f"unhandled redirect {r.status_code}"

    text = r.text or ""
    lower = text.lower()

    # Must mention jobs/careers vocabulary on the page
    if not JOB_TEXT.search(text):
        return name, url, "FAIL", "no jobs-related keywords on page"

    # Count job-indicator links in the HTML
    link_matches = 0
    for ind in JOB_INDICATORS:
        if ind in lower:
            link_matches += lower.count(ind)

    if link_matches == 0:
        # Page loads and mentions jobs but has no detectable job-posting links.
        # Could be JS-rendered - flag as WEAK but don't auto-add.
        return name, url, "WEAK", f"page loads, but no job-posting links detected (may need Playwright)"

    return name, url, "PASS", f"{link_matches} job-indicator hits"


def main():
    results = []
    with ThreadPoolExecutor(max_workers=15) as ex:
        futures = {ex.submit(verify, n, u): (n, u) for n, u in CANDIDATES}
        for fut in as_completed(futures):
            results.append(fut.result())

    results.sort(key=lambda x: (x[2], x[0]))
    passed = [r for r in results if r[2] == "PASS"]
    weak = [r for r in results if r[2] == "WEAK"]
    failed = [r for r in results if r[2] == "FAIL"]

    print(f"\n=== VERIFICATION RESULTS ===")
    print(f"PASS: {len(passed)}")
    print(f"WEAK: {len(weak)} (loads but no job links - probably JS-rendered)")
    print(f"FAIL: {len(failed)}")
    print()

    print("=== PASSED (will be added) ===")
    for n, u, _, d in passed:
        print(f"  {n}: {u} ({d})")

    print(f"\n=== WEAK (NOT added - may need Playwright type) ===")
    for n, u, _, d in weak:
        print(f"  {n}: {u} ({d})")

    print(f"\n=== FAILED (NOT added) ===")
    for n, u, _, d in failed:
        print(f"  {n}: {u} ({d})")

    # Write rejected log
    with open("rejected_candidates.txt", "w") as f:
        f.write("# Candidates that did NOT pass verification\n\n")
        for n, u, status, detail in weak + failed:
            f.write(f"[{status}] {n} | {u} | {detail}\n")

    if not passed:
        print("\nNo candidates passed. companies.yaml not modified.")
        return

    # Load existing companies.yaml
    with open("companies.yaml", "r") as f:
        config = yaml.safe_load(f)

    existing_names = {c["name"].lower() for c in config["companies"]}
    existing_urls = {c["url"].lower().rstrip("/") for c in config["companies"]}

    added = 0
    skipped = 0
    for name, url, _, _ in passed:
        # Strip "(alt)" suffixes for clean names
        clean_name = name.split(" (alt)")[0]
        if clean_name.lower() in existing_names:
            skipped += 1
            continue
        if url.lower().rstrip("/") in existing_urls:
            skipped += 1
            continue
        config["companies"].append({
            "name": clean_name,
            "type": "html_links",
            "url": url,
        })
        existing_names.add(clean_name.lower())
        existing_urls.add(url.lower().rstrip("/"))
        added += 1

    # Write back with consistent formatting
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

    print(f"\n=== SUMMARY ===")
    print(f"Added {added} verified companies to companies.yaml")
    print(f"Skipped {skipped} (already present)")
    print(f"Total companies now: {len(config['companies'])}")
    print(f"See rejected_candidates.txt for what was dropped.")


if __name__ == "__main__":
    main()
