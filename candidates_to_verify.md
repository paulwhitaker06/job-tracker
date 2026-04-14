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
