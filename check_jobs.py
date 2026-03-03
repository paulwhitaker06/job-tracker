import requests
import yaml
import hashlib
import json
from bs4 import BeautifulSoup
import os

SEEN_FILE = "seen_jobs.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def hash_job(url):
    return hashlib.md5(url.encode()).hexdigest()

def get_html_links(company):
    r = requests.get(company["url"], timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "link_contains" in company:
            if company["link_contains"] in href:
                links.add(href)
        else:
            links.add(href)

    return links

def get_ashby_jobs(company):
    r = requests.get(company["url"], timeout=30)
    data = r.json()
    links = set()
    for job in data.get("jobs", []):
        links.add(job.get("jobUrl"))
    return links

def main():
    with open("companies.yaml") as f:
        config = yaml.safe_load(f)

    seen = load_seen()
    new_jobs = []

    for company in config["companies"]:
        print(f"Checking {company['name']}")

        try:
            if company["type"] == "html_links":
                jobs = get_html_links(company)
            elif company["type"] == "ashby_api":
                jobs = get_ashby_jobs(company)
            else:
                print("Skipping unsupported type for now")
                continue

            for job in jobs:
                job_hash = hash_job(job)
                if job_hash not in seen:
                    seen.add(job_hash)
                    new_jobs.append((company["name"], job))

        except Exception as e:
            print(f"Error with {company['name']}: {e}")

    if new_jobs:
        print("\nNEW JOBS FOUND:")
        for name, url in new_jobs:
            print(f"{name}: {url}")
    else:
        print("\nNo new jobs today.")

    save_seen(seen)

if __name__ == "__main__":
    main()
