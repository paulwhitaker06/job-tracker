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
| **ORBES** | https://orbes.space/careers | Outreach radar 71.5; pre-seed inspection sats; apply.workable.com/orbes account exists but unconfirmed as theirs, zero jobs | parked 2026-09-07, radar backlog audit |
| ~~Gilat Satellite Networks~~ | https://www.gilat.com/career/ | Radar 34.0; careers behind Sucuri JS challenge, old Comeet board dead; needs a real browser | VERIFIED 2026-09-09, added to companies.yaml (Comeet board 39.005, 37 jobs incl. two Director BD roles) |
| **Seagate Space** | https://seagatespace.com/ | Radar 79.0; 2025 offshore-launch startup, site has NO careers page, LinkedIn-only hiring | parked 2026-09-07, radar backlog audit |
| **Sophia Space** | https://sophia.space/ | Radar 69.5; no careers page, jobs via LinkedIn/ZipRecruiter only | parked 2026-09-07, radar backlog audit |
| **Starfighters Space** | https://starfightersspace.com/ | Radar 51.5; no careers section on site, no ATS found | parked 2026-09-07, radar backlog audit |
| **NordSpace** | https://www.nordspace.ca/careers | Radar 56.5; careers page is an unfinished Webflow template, real path careers@nordspace.com | parked 2026-09-07, radar backlog audit |
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
| **Skynopy** | https://www.welcometothejungle.com/en/companies/skynopy/jobs | Payload 2026-09-10: launched Global AKAR with Eutelsat, a software-defined ground network; ground-station-as-a-service for LEO operators, 15+ stations, EUR 15M raised | parked 2026-09-10, daily newsletter harvest |
| **Charter Space** | https://www.charter.space/careers | Payload 2026-09-10 (paid sponsor slot, not editorial): US space insurance brokerage; careers page returns 200 but lists zero roles | parked 2026-09-10, daily newsletter harvest |
| **Venturi Space** | none found | Payload 2026-09-10: unveiled the ALTA LUNA lunar utility vehicle; neither venturi-space.com nor venturispace.com resolved from probe | parked 2026-09-10, daily newsletter harvest |
| **UNIVITY** | none found | Payload 2026-09-10: claims first mmWave 5G NTN connection with shared uplink and downlink spectrum; real domain unidentified, univity.space is parked for sale | parked 2026-09-10, daily newsletter harvest |
| **Vaya Defense and Space** | none found | Payload 2026-09-10: hybrid propulsion, signed an MoU with Starfighters Space for suborbital air-launch; no board located | parked 2026-09-10, daily newsletter harvest |
| **Interstellar Mapping** | none found | Payload 2026-09-10: co-founder in the Off World panel lineup; commercial status unconfirmed, weakest candidate in this batch | parked 2026-09-10, daily newsletter harvest |
| **Thales Alenia Space** | none found | Payload 2026-09-22: signed an MoU with Dhruva Space on LEO constellations and ground infrastructure; European space prime. thalesaleniaspace.com/en/careers returns 404 and no ATS slug resolved | parked 2026-09-22, daily newsletter harvest |
| **ORBITInsure** | none found | Payload 2026-09-22: joined the Commercial Space Federation; space insurance, a risk and data pricing vertical adjacent to the AXA and British Marine deals. orbitinsure.com did not resolve at all, likely no public site under that spelling | parked 2026-09-22, daily newsletter harvest |

Re-check notes, 2026-09-09 radar cross-check (all still parked, same outcome as 2026-09-07):
- **ORBES** is not European and not Earth observation: it is a Los Angeles Techstars company building in-space inspection and maintenance robots. orbes.space/careers is a real page with one open role, but applications go to an email address and there are zero per job links.
- **Seagate Space** has nothing to do with Seagate Technology or data storage. It is a 2025 St. Petersburg FL startup building modular offshore sea launch platforms, with a Firefly co-design agreement. Site has no careers page at all.
- **NordSpace** is an environment failure rather than a company failure: nordspace.ca serves a TLS stack this machine cannot negotiate, so the board could not be read. Worth one retry from a machine with modern OpenSSL. Do not use nordspace.com, it is a stale Webflow template.
- **Sophia Space**, **Mission Space** and **Starfighters Space** have no careers page on their own sites, confirmed against each site's sitemap. LinkedIn is the only route.
- **GD1** is confirmed a New Zealand venture fund, not an operating company. Its portfolio aggregator at careers.gd1.vc/jobs is live but would pollute companies.yaml with unrelated roles.
- **GHGSat** is NOT missing from companies.yaml; it is already tracked under the name "GHG Sat" (workable_api). The outreach radar spells it without the space.

Re-check notes, 2026-09-10 radar cross-check (no growth; every hit was an alias or spelling artifact, or already parked):
- The cross-check flagged 18 proactive_targets as missing from companies.yaml. Five were subsidiary naming of tracked parents (ICEYE US, EnduroSat USA, Kepler Communications US, Anduril Maritime, EarthDaily Analytics) and three were tracked under different strings (Apex is "Apex Space", Umbra is "Umbra Space (Umbra Lab)", ULA is "United Launch Alliance").
- The remaining nine were the known backlog. GHGSat is tracked as "GHG Sat"; Starlab Space resolves to the Voyager Technologies board; GD1 is a venture fund; Seagate Space, Sophia Space, Mission Space, Starfighters Space and NordSpace stay parked with the same outcomes as 2026-09-07.
- ORBES row URL corrected to orbes.space/careers (www.orbes.us was the wrong domain). orbes.space/careers is a real Framer page with one open role, but applications go to a mailto and there are no per job URLs, so it stays parked rather than becoming html_links. It would fit the manual_check convention if that is wanted.
- NordSpace row URL corrected to nordspace.ca (the .com is a stale template). The .ca TLS failure was reproduced with OpenSSL 3.6.3, LibreSSL curl, Python urllib and WebFetch, so it is a Webflow bot filter rejecting non-browser clients, not a local TLS stack problem.
- Starlab Space: the bare domain starlab.space is now a GoDaddy for-sale parked page. The live site is starlab-space.com. If the dashboard radar card links to starlab.space, that link is dead.
| **T. Rowe Price** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **AT&T Business** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Amazon Leo** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Vaya Defense & Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **NewOrbit Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Genesia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Tenchijin** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **iQPS** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Deutsche Telekom IoT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **stc group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Graviron Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-12 |
| **Office of Energy Dominance Financing (EDF/LPO)** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Southern Company** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Pattern Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Westinghouse** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Ford** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Solyndra** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **ARC Ride** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Carrum Mobility** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Molten Salt Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Jaipur Robotics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Rebaba** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Circolife** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **FRYTE Mobility** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Veridue AI** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **DigitalPaani** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Elia Transmission Belgium** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Anesco** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Siltworm** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **ENERPARC AG** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Molten Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Shine** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Fortum** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Jet Zero Australia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Carbon Neutral Fuels** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-14 |
| **Space42** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-15 |
| **Elveo Mobile** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-15 |
| **Mitsubishi Heavy Industries** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-15 |
| **ColliMate Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-15 |
| **The Fermi Explorer Mission** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-15 |
| **Brightband** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-16 |
| **Mistral** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-16 |
| **Ecosmic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-17 |
| **Dassault** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Argo Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **EQT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astra** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Mazama** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kanin Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LineVision** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Branch Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Nomos** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CorePower Magnetics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MCatalysis** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ferm Labs** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Depotcharge** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **PyroCCS** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Heron Power** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Tavion** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **BioValue** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kanadevia Inova** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Wittington Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Vantor** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Quantum Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Airbus Defence and Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SEOPS** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Virgin Galactic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ATMOS Space Cargo** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astrobotic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Reflect Orbital** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CesiumAstro** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astrolight** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AeroVironment** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Interlune** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ElevationSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **PlanetiQ** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Satlyt** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astroscale** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Venus Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Bellatrix Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kratos Defense & Security Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Seraphim Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Unibap** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SWISSto12** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orbital Matter** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Marlan Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Xoople** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Varda** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Energy Aspects** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AstroForge** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Juno Propulsion** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **T-Minus Engineering** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Remondo** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **OQ Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MinoSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **R-Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Tumbleweed** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ISISPACE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Weather Stream** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Beyond Gravity** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NUVIEW** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ovzon** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ArkEdge Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kratos Defense and Security Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Skyroot Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Optera** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **FLEXELL SPACE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Instinct Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Symphony Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lunar Forge** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ACME Solar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hadrian** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Frontier Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Southern Launch** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Paragon Space Development** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Fortastra** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TransAstra** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lynk Global** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hydrostor** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LandSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **All Points Logistics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Blue Canyon Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sedaro** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Proteus Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kall Morris** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Voltus** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sage Geosystems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kongsberg NanoAvionics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Nightwing** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **PiLogic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **City Labs** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **The Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Neumann Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orbotic Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Edge Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **KSAT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lockheed Martin Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Quaise Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Greenvolt** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Apollo Atomics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Swift Current Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **InspeCity** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LambdaVision** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Gravitics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Galactic Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Creotech Instruments** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kreios Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **HyImpulse Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **HyPrSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **X-Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Holtec** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Bluecore Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aukera Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Tesla** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sirius Space Services** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| ~~HEO~~ | https://heo.breezy.hr/ | Payload intel mention; on the outreach radar pipeline. Payload 2026-09-22: closed a $25M Series B led by Beaten Zone VP, 50+ sensors on orbit as hosted payloads, tripling revenue and hiring | VERIFIED 2026-09-22, added to companies.yaml (heo.breezy.hr, 7 open roles across Sydney and Arlington VA) |
| **Maverick Space Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Icarus Robotics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ispace US** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Emerald AI** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sceye** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Pachama** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Array Labs** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AXA Digital** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Telespazio Ibérica** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MethaneSAT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CTrees** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Taylor Geospatial** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Syngenta** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sarvam** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Enagás** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orbital Eye** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Magellium Artal Group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LEAP** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **WarpWare** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lonestar Data Holdings** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Verizon / T-Mobile / AT&T** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Blacknight Space Labs** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aireon** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **OHB Space UK** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Eta Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Potomac Database Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ThinKom** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Solestial** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Zenk Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **QuesTek Innovations** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NOVI Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Spartan Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SITAEL** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **OHB Czechspace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Digantara** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Preligens** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aitech Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Stellar Alpina** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Markets** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Applied Aerospace & Defense** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **American Airlines** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Archangel Lightworks** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Solar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Observable Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hermeus** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Revolv Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TelePIX** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SFL Missions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Argotec** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SparkSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sutherland Spaceport** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Denmar Technical Services** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Alen Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Infinite Orbits** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Vortex-io** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Esper** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Arkadia Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Pilot Photonics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TerraSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Tilebox** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Applied Atomics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Forge** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Calian** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **EDGE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sky Perfect JSAT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rocket One** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **STMicroelectronics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astroport Space Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Photocentric** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AMG Critical Materials** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Jio Platforms** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Spark Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SPACEBEL** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **HENSOLDT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ubotica Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ANT61** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Vyoma** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SpaceComputer** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SHIELD SPACE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Verde Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **QOSMIC** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Fleet Space Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orbital Composites** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Nebex** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Honeywell Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **RSAT Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Neo Space Group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ImageSat** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MSCI** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Changguang Satellite Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Solstar Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rakuten Group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ravee Optics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hongqing Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sybilla Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **EMXYS** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NearSpace Launch** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Novaspace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Auxilium Biotechnologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **BioOrbit** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Outpost Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Pulse Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NGC Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Parabilis Space Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **DayOne** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NScale** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Fervo** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Proxima Fusion** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hippo Harvest** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Fleek** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Axle Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **e-peas** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hephae Energy Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Bohr Energie** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Fuchs & Eule** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Polysense** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Dogtooth Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aardaia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Porelio** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Milo Drive** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Wildfire Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **GIGA Storage** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Opdenergy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **General Fusion** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **IPoint** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Harmony Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lemvig Biogas** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **United Solar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Changguang Satellite Technology Co** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Spire** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Spinifex Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Black Sky Industries** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Northrop Grumman Australia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lockheed Martin Australia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kongsberg Defence Australia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Earth Daily** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Draper** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Norway** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SpaceIQ** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **VXB** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Frontier Airlines** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **KULR Technology Group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Canadensys Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Satellite Orbital Access and Removal** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Antaris** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **EDGE Group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Airbus Netherlands** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AgniKul Cosmos** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Dhruva Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Martin Materials Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rize** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Applied Computing** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NxLite** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Gridcog** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **E3 Electric.Ai** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hyperion Robotics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **BiofuelCircle** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Visibuilt** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Optiflux** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NextGO Epi** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **BZero Materials** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **StratX** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Masdar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **OMV** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TotalEnergies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Positive Zero** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Blueleaf Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **PureSky Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Carbyon** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CATL** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Stryten Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Airhive** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Verdane** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **deltaVision** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rogue Space Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LegendSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Extellis** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Planet Labs UK** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **bluShift Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Florida** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LEO Biosciences** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **RootMatrix Bio** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **The Skyway Organization** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ORiS** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **KBR** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space VC** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Type One Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MDA Space UK** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rivada Space Networks** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Puli Space Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Deloitte** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Zenno Astronautics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Spectra Studios** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Whipsmart Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Contrivian** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Trimble Military and Advanced Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **DigitalBlast** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Cyberspace Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **QuantX Labs** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Holland & Knight** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **U.S. Electrodynamics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Unibap Space Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CuspAI** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Asuene** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Greenjets** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MoA Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Phytokana Ingredients** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Circular Materials** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CullBeck** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Raydean** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Plantopia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Contact BioSolutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TaiSan** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aampere** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Fidra Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AMPYR Distributed Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lug+Carrie** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Prevalon Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Secaro** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Royal Uranium** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **HAMR Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Globalstar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SES Space & Defense** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Outlier Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aalyria** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Honeybee Robotics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Phoenix Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Slooh** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Broadside** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Stars Harmony** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Genesis Space Flight Laboratories** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **All Point Logistics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Vermeer** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Advanced Rocket Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aqtar Space Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Revoy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Nuclear Turbines** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Quercus Biosolutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **FAST Metals** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Agscent** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Apolownia** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Enexis** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Grenergy Renovables** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Gotion Power Morocco** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SustainCERT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SDP Energie** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Varta** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **JFE Steel** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hughes Satellite Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AE Industrial Partners** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rocketdyne** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orbital Sentry** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Neuraspace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Outpost** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Rubicon Space Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Frontgrade** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Endeavor Optical Networks** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Systems & Technology Research** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Moog** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SpeQtral** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orienspace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Starbase Europe** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **HispaSat** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **IonQ** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **United Semiconductors** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Deepfire** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astroscale US** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Base Power** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Mariana Minerals** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ore Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Advanced Electric Machines** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Matel Motion and Energy Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Plantible** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Critical Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **BioScout** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MaintainX** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ENTACT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NexTC** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sono Motors** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Energy Dome** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Invinity** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CMBlu** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **XL Batteries** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Terraflow Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **RWE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Siemens Gamesa** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Mosaic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Bimbo Group** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Intermap Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **PCI Geomatics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Verisk** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **McKenzie Intelligence Services** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Schneider Electric** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **IENAI SPACE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Wildstar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **VinSpace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Exosat** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Omnispace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Cursor** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Jariet Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Gravitilab Aerospace Services** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Amazon LEO for Government** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Alva** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Standard Nuclear** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **BWXT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Oklo** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Deployable Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aalo** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Nano Nuclear** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Terra Innovatum** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Hadron Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Deep Fission** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NuCube** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Yulu** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ranchbot Monitoring Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AGent Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Riven Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Inaara NeoFoods** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **European Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Global Advanced Metals** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **5E Advanced Materials** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Aegeus Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **LEAP India** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Dynatec Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Kinertic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Electric GT** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Genomatica** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **WovenEarth Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Energy Capital Partners** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **NEOM** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **De Nora** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **P2H2** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Thyssenkrupp** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space Angel** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Eoptic** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sierra Nevada** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Auriga Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Letara** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Antares Nuclear** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **EO Solutions** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Method Security** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ThinkOrbital** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Castelion** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Eartheye Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Phantom Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Xingkan Jiuzhou Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Spherical Systems** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Deep Blue Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Also.** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ampaire** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sonic Fire Tech** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **RockRose Risk** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Companion.energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Computomics** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Oceanloop** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Oshen** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **GreenJoules** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Mafix** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SnerpaPower** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Key Capture Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Power Info** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **RenuTrak** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Georgia Power** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Plug Power** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Shine Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **OrbitAID Aerospace** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Star Catcher Industries** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Shield AI** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **VEOWARE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Lonestar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Odin Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Arkisys** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Ethos Space Resources** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Tendeg** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Miratlas** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **RIDE!** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Sarmony** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Addvalue** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Cesium Astro** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Astrum Space** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Space One** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Phi Earth Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Telespazio France** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TraCSS** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MDA Space LaunchPad Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Diffraqtion** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Presidio Ventures** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **SES Satellites** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AnalySwift** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Gatik** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Airbound** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Voya Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Matter Motors** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Breedr Impact** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Vitalfluid** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Certain Energy** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **TerraBlaster** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **MAASH** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CarbonStrong** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **AmpIn Energy Transition** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **CF Industries** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ElectraLith** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Heidelberg Materials** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Physical Superintelligence** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Velocity Government Relations** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Teledyne Space Imaging** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Orbion Space Technology** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Canopy Aerospace & Defense** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Quindar** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Yank Technologies** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Seraphim** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ispace-EUROPE** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **Eutelsat OneWeb** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
| **ST Engineering iDirect** | | Payload intel mention; on the outreach radar pipeline | probes missed 2026-09-21 |
