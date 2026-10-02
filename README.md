# job-tracker

`check_jobs.py` runs once a day in GitHub Actions (`.github/workflows/daily.yml`).
It reads every board in `companies.yaml`, works out which postings are new, and
emails a `[Job Tracker]` digest of the new ones whose title scores above 0.
`companies.yaml` is the single list of boards to scan.

## Title filter

A posting goes into the digest only if `score_title` gives its title more than
0. The score is the sum of three keyword buckets, each capped: seniority (5),
function (8) and domain (10). Keywords match whole words, so the plural
"partnerships" does not match "Partnership Manager"; each form needs its own
entry.

- `SENIORITY_KEYWORDS`, `FUNCTION_KEYWORDS` and `DOMAIN_KEYWORDS` are matched
  against the title and the posting URL together.
- `TITLE_ONLY_SENIORITY_PATTERNS` and `TITLE_ONLY_FUNCTION_PATTERNS` are matched
  against the title alone. Short or ambiguous tokens go here (`bd`, `bdm`,
  `svp`, `evp`, `president`, singular `partnership`, `partner manager`, the
  government-sales sense of `capture`), because they turn up in URLs and
  company slugs for unrelated reasons.
- A title with a junior token (intern, junior, associate, coordinator,
  specialist and so on) scores 0 unless its function or domain bucket reaches 4.
  "Associate Director" and "Associate Vice President" are not junior.
- British spellings are listed next to the American ones (`defence`,
  `commercialisation`).
- "Bid Manager" is left out on purpose.

A posting stored with score 0 is scored again each time the scraper sights it
on its board, so after a keyword change the postings that are still live and
now score above 0 appear in the next digest, once. Postings that have dropped
off their board do not come back.

## State files

| File | What it holds |
| --- | --- |
| `seen_jobs.json` | Every item the scraper has seen, kept for 90 days after its last sighting. |
| `company_health.json` | Per board: runs, failure streak, empty streak, last date it showed a real posting. |
| `search_cache.json` | `last_manual_recheck`, the 30-day gate for the monthly `manual_check` re-probe. |

Entries in `seen_jobs.json` can carry two flags. Both mean "not a posting, never
emailed, do not fetch again":

- `junk_url`: an aggregator root or browse page.
- `garbage_title`: the title is navigation text ("Careers", "Apply now") or
  empty. If it is empty because the title fetch failed, the entry also has
  `title_tries` and the fetch is retried on later runs, up to 5 runs in total.
  If a later scrape carries a real title, the entry becomes a normal posting
  and goes into that day's digest.

Anything that counts postings in `seen_jobs.json` should skip entries with
either flag.

## Board health

A board counts as producing on a run only if it showed at least one real
posting, new or already seen. These do not count:

- junk listing URLs and garbage titles (the two flags above);
- the board's own configured URL, when it comes back as a plain link;
- plain links whose page title is a careers or listing page title
  ("Careers at Acme", "Job Openings", "Search Openings") or just the company
  name.

So a board that returns only its careers landing page or its menu links is
empty, and after 7 runs it is listed as "never produced a real posting".
These tests are used for health only. They never remove an item from
`seen_jobs.json` or from the digest.

Health for a successful scrape is recorded after titles have been fetched.
The fields in `company_health.json` are unchanged: `first_tracked`, `runs`,
`fail_streak`, `empty_streak`, `last_ok`, `last_nonempty`, `crossed_30_on`.
`last_nonempty` now means the last date with a real posting. Stamps written by
the older counting (any link counted) are corrected on the first run: a recent
`last_nonempty` with no real stored posting behind it is moved back to the
last real sighting, or removed.

## Boards needing attention

Both parts of the digest email (plain text and HTML) carry this section, on
"No new jobs" days too. It lists, worst first:

1. boards whose scrape has failed 3 or more runs in a row;
2. boards that produced before and have shown no real posting for 30 or more runs;
3. boards that have never produced a real posting in 7 or more runs.

Within each group the longest streak comes first. The digest shows the first 20
and states the total. The full list is in the run log.

## If the digest email fails

The digest is sent first and state is written second. If the send fails, or the
mail secrets are missing, `check_jobs.py` writes neither `seen_jobs.json` nor
`company_health.json` and exits non-zero. The workflow then skips its commit
step and sends its failure notification. The next run finds the same postings
as new and sends them.

A local run with no mail settings at all is a dry run: nothing is sent and
state is written as usual.

## Retired

The weekly Google search sweep was removed on 2026-10-02. Its API (Google
Custom Search JSON) returned HTTP 403 on every query from 2026-07-10 and never
produced a result. The `GOOGLE_CSE_KEY` and `GOOGLE_CSE_ID` repository secrets
are no longer read and can be deleted.
