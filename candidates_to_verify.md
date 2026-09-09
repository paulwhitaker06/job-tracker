# Candidates to Verify Manually

48 candidates that didn't auto-verify (12 WEAK + 36 FAIL). Sorted by fit for Paul's profile: Director/VP commercial/BD/partnerships at mission-driven data companies, strong preference for ocean/maritime/climate with non-profit tolerance. Defense/intel hard-excluded.

**How to use this file:**
1. Work top to bottom — high priority first.
2. For each entry, find the real careers URL (click through from the main site, check their LinkedIn "About" page, or Google "{Company} careers").
3. Once you have a verified URL, add it:
   ```
   python3 add_company.py "Company Name" "https://verified.careers.url"
   ```
4. Cross off entries in this file as you go (just delete the line or add `~~strikethrough~~`).

---

## TIER 1 — High Priority (ocean/climate/CDR, strongest fit)

These are most worth your time. If only 10 get verified, pick these.

| Company | Candidate URL | Why it fits | Status |
|---|---|---|---|
| **Vesta** | https://www.vesta.earth/careers | Ocean CDR — literally the intersection of your ocean background + commercial CDR growth | FAIL 404 |
| **Running Tide** | https://www.runningtide.com/careers | Ocean carbon removal, partnerships with Microsoft. Fits GFW-alum profile perfectly | FAIL conn |
| **Ebb Carbon** | https://www.ebbcarbon.com/careers | Ocean alkalinity enhancement — commercial CDR | FAIL 404 |
| **Seabound** | https://www.seabound.co/careers | Ship-based carbon capture — maritime + CDR | FAIL 404 |
| **Nautilus Labs** | https://nautiluslabs.com/careers/ | Maritime AI, fleet optimization | FAIL conn |
| **Shone** | https://www.shone.ai/careers | Autonomous shipping | FAIL no keywords |
| **IUCN** | https://www.iucn.org/about-iucn/jobs | Largest env NGO, oceans program matches GFW work | WEAK (JS-rendered) |
| **Fleetzero** | https://fleetzero.com/careers | Electric container shipping | FAIL 404 |
| **Salient Predictions** | https://salientpredictions.com/careers/ | Maritime/weather subseasonal forecasting | FAIL 404 |
| **AER Atmospheric Research** | https://www.aer.com/careers/ | Maritime/climate analytics, commercial | FAIL no keywords |

## TIER 2 — High Priority (CDR / climate VC portfolios / climate NGOs)

| Company | Candidate URL | Why it fits | Status |
|---|---|---|---|
| **Holocene** | https://www.holocene.company/careers | Amine-based DAC | FAIL conn |
| **Spiritus** | https://spiritus.earth/careers | Direct air capture, ex-Los Alamos | FAIL conn |
| **Verdox** | https://verdox.com/careers/ | Electrochemical CDR | FAIL 404 |
| **Noya** | https://www.noya.co/careers | DAC using existing cooling towers | FAIL 404 |
| **Elemental Excelerator Portfolio** | https://jobs.elementalexcelerator.com/jobs | Climate accelerator — portfolio boards produce high volume | FAIL 404 |
| **MCJ Collective Portfolio** | https://jobs.mcjcollective.com/jobs | My Climate Journey — ~600 portfolio companies | FAIL conn |
| **Voyager Ventures Portfolio** | https://jobs.voyagervc.com/jobs | Climate VC Getro board | FAIL conn |
| **World Fund Portfolio** | https://jobs.worldfund.vc/jobs | European climate VC | FAIL conn |
| **Systemiq Capital Portfolio** | https://jobs.systemiq.earth/jobs | Climate investment firm | FAIL conn |
| **SOSV Portfolio** | https://jobs.sosv.com/jobs | HAX/IndieBio — hard tech accelerator | FAIL conn |
| **At One Ventures Portfolio** | https://jobs.atoneventures.com/jobs | Climate VC | WEAK (JS-rendered) |
| **Moore Foundation** | https://www.moore.org/careers | Gordon & Betty Moore — marine conservation funding | WEAK (JS-rendered) |
| **MacArthur Foundation** | https://www.macfound.org/about/careers | Climate solutions grants | WEAK (JS-rendered) |
| **Stockholm Environment Institute** | https://www.sei.org/about-sei/vacancies/ | Climate policy/data research | FAIL 403 |
| **UNEP** | https://www.unep.org/jobs | UN Environment Programme | FAIL 403 |
| **Coral Reef Alliance** | https://coral.org/careers/ | Marine conservation | FAIL 404 |

## TIER 3 — Medium Priority (geospatial SaaS, agtech, weather)

Your core expertise but less mission-driven.

| Company | Candidate URL | Why it fits | Status |
|---|---|---|---|
| **Placer.ai** | https://www.placer.ai/careers | Location intelligence — your domain | FAIL 404 |
| **Ceres Imaging** | https://www.ceresimaging.net/careers/ | Aerial imagery for ag | FAIL 404 |
| **Understory** | https://understoryweather.com/careers/ | Hyperlocal weather/insurance | FAIL 404 |
| **Carbon Robotics** | https://carbonrobotics.com/careers | AI-powered farm equipment | WEAK (JS-rendered) |
| **Indigo Ag** | https://www.indigoag.com/careers | Soil carbon + ag data | WEAK (JS-rendered) |
| **BeeHero** | https://beehero.io/careers/ | Pollination data (Israeli agtech) | WEAK (JS-rendered) |
| **Kilimo** | https://kilimo.com/careers/ | LATAM precision ag | FAIL 404 |
| **Greeneye Technology** | https://www.greeneye.technology/careers/ | AI precision spraying | FAIL conn |
| **NatureServe** | https://www.natureserve.org/careers | Biodiversity data | WEAK (JS-rendered) |

## TIER 4 — Lower Priority (emissions, ocean adjacent)

| Company | Candidate URL | Why it fits | Status |
|---|---|---|---|
| **Kairos Aerospace** | https://kairosaerospace.com/careers/ | Methane detection from planes | FAIL 403 |
| **Bridger Photonics** | https://www.bridgerphotonics.com/careers | Methane detection lidar | WEAK (JS-rendered) |
| **LongPath Technologies** | https://www.longpathtech.com/careers | Methane monitoring | FAIL 404 |
| **Project Canary** | https://www.projectcanary.com/careers/ | Emissions certification | WEAK (JS-rendered) |
| **Amogy** | https://amogy.co/careers/ | Ammonia-powered shipping | WEAK (JS-rendered) |
| **ZeroNorth** | https://zeronorth.com/careers/ | Shipping emissions/optimization | WEAK (JS-rendered) |
| **Aquabyte** | https://aquabyte.ai/careers/ | Aquaculture computer vision | FAIL 404 |

## TIER 5 — Skip (defense/federal hard-exclusion or misaligned)

Your profile hard-excludes defense/intel. NOAA/USGS are government — slow hiring cycles and civil-service pay bands unlikely to fit a Director role at your level.

| Company | Reason to skip |
|---|---|
| Leidos | Defense contractor — hard exclusion |
| SAIC | Defense contractor — hard exclusion |
| NOAA | Government civil service |
| USGS | Government civil service |

---

## WEAK Entries — These pages exist but may need `playwright` type

The URL below returns 200 with "jobs"/"careers" keywords, but the requests-based scrape couldn't find any job-posting links (usually because the page is JavaScript-rendered). If you want to include these, add them with `playwright` type:

```
python3 add_company.py "Amogy" "https://amogy.co/careers/" playwright
```

Candidates that may work with playwright: At One Ventures Portfolio, BeeHero, Bridger Photonics, Carbon Robotics, IUCN, Indigo Ag, MacArthur Foundation, Moore Foundation, NatureServe, Project Canary, ZeroNorth.

Note: expect most of these to fail even with Playwright — JS-rendered pages often need custom handling. Only worth enabling if you really want that company tracked.

## Parked from Payload intel (ATS probes missed; verify manually)

| Company | Candidate URL | Why it fits | Status |
|---|---|---|---|
| **ORBES** | https://www.orbes.us | Outreach radar 71.5; pre-seed inspection sats; apply.workable.com/orbes account exists but unconfirmed as theirs, zero jobs | parked 2026-09-07, radar backlog audit |
| ~~Gilat Satellite Networks~~ | https://www.gilat.com/career/ | Radar 34.0; careers behind Sucuri JS challenge, old Comeet board dead; needs a real browser | VERIFIED 2026-09-09, added to companies.yaml (Comeet board 39.005, 37 jobs incl. two Director BD roles) |
| **Seagate Space** | https://seagatespace.com/ | Radar 79.0; 2025 offshore-launch startup, site has NO careers page, LinkedIn-only hiring | parked 2026-09-07, radar backlog audit |
| **Sophia Space** | https://sophia.space/ | Radar 69.5; no careers page, jobs via LinkedIn/ZipRecruiter only | parked 2026-09-07, radar backlog audit |
| **Starfighters Space** | https://starfightersspace.com/ | Radar 51.5; no careers section on site, no ATS found | parked 2026-09-07, radar backlog audit |
| **NordSpace** | https://www.nordspace.com/careers | Radar 56.5; careers page is an unfinished Webflow template, real path careers@nordspace.com | parked 2026-09-07, radar backlog audit |
| **Mission Space** | https://www.mission.space/ | Radar 56.0; space-weather co, no careers page at all, LinkedIn-only | parked 2026-09-07, radar backlog audit |
| ~~Simera Sense~~ | https://simerasense.com/ | Payload 2026-09-08: hyperspectral EO payload for Galaxia; South African optical payload maker, commercial-stage EO hardware; site unreachable from probe, no ATS found | VERIFIED 2026-09-09, added to companies.yaml (simera-sense.breezy.hr, 5 open roles) |
| ~~Galaxia~~ | https://www.galaxia.ca/ | Payload 2026-09-08: Canadian EO constellation buying a hyperspectral payload from Simera Sense; site unreachable from probe, no ATS found | VERIFIED 2026-09-09, added to companies.yaml (gx.space/careers, 15 listings incl. 3 regional BD Manager roles) |
| ~~Orbital Lasers~~ | https://www.orbitallasers.jp/ | Payload 2026-09-08: Japanese laser debris-removal and spaceborne optics company, equity investment in LogistLab; site unreachable from probe, no ATS found | VERIFIED 2026-09-09, added to companies.yaml (hrmos.co board, 32 open roles) |
| **Aegis Aerospace** | https://aegisaero.com/careers | Payload 2026-09-08: DoD task order for defense payload development; hosted-payload integrator; careers page returns 406 to probes, no ATS found | parked 2026-09-08, daily newsletter harvest |
| ~~Maritime Launch Services~~ | https://www.maritimelaunch.com/careers | Payload 2026-09-08: Spaceport Nova Scotia agreement with Isar Aerospace; careers page is plain HTML with no ATS links | VERIFIED 2026-09-09, added to companies.yaml (maritimelaunch.com/careers, 6 listings incl. COO and CFO) |
| **Project-S** | https://www.project-s.space/careers | Payload 2026-09-08: German SSA startup out of stealth with multimillion-euro backing, in-orbit demo next month; careers page has no ATS links yet | parked 2026-09-08, daily newsletter harvest |
| ~~Starlab Space~~ | https://apply.workable.com/starlab/ | Outreach radar; Workable account named Starlab exists but lists zero jobs, unconfirmed as theirs | RESOLVED 2026-09-09, no separate board: Starlab hires through the Voyager Technologies Greenhouse board already in companies.yaml |
| **GD1** | https://gd1.vc/ | Outreach radar; New Zealand venture fund, not an operating company, no careers board expected | parked 2026-09-08, radar cross-check |
| **SaxaVord Spaceport** | https://saxavord.com/recruitment/ | Payload 2026-09-09: receiving 30M GBP from the UK government plus 30M GBP private; UK vertical launch spaceport on Unst, Shetland. Recruitment page loads but states no positions currently available, and past postings sit at top level slugs with no stable substring | parked 2026-09-09, daily newsletter harvest |
| **LogistLab** | https://logistlab.biz/recruit/ | Payload 2026-09-08: named in an Orbital Lasers equity investment for spaceborne telescopes and optics. The only company of this name is a Kyoto optics R and D venture (precision mirrors, Seimei telescope heritage); its recruit page links four role titles to one generic page, so there is no per job URL. Re-read the Payload item before adding, the name may refer to a firm with no web presence yet | parked 2026-09-09, daily newsletter harvest |

Re-check notes, 2026-09-09 radar cross-check (all still parked, same outcome as 2026-09-07):
- **ORBES** is not European and not Earth observation: it is a Los Angeles Techstars company building in-space inspection and maintenance robots. orbes.space/careers is a real page with one open role, but applications go to an email address and there are zero per job links.
- **Seagate Space** has nothing to do with Seagate Technology or data storage. It is a 2025 St. Petersburg FL startup building modular offshore sea launch platforms, with a Firefly co-design agreement. Site has no careers page at all.
- **NordSpace** is an environment failure rather than a company failure: nordspace.ca serves a TLS stack this machine cannot negotiate, so the board could not be read. Worth one retry from a machine with modern OpenSSL. Do not use nordspace.com, it is a stale Webflow template.
- **Sophia Space**, **Mission Space** and **Starfighters Space** have no careers page on their own sites, confirmed against each site's sitemap. LinkedIn is the only route.
- **GD1** is confirmed a New Zealand venture fund, not an operating company. Its portfolio aggregator at careers.gd1.vc/jobs is live but would pollute companies.yaml with unrelated roles.
- **GHGSat** is NOT missing from companies.yaml; it is already tracked under the name "GHG Sat" (workable_api). The outreach radar spells it without the space.
