# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/). Feature PRs add a line under
`## [Unreleased]`; only `make release` turns it into a versioned section.

## [Unreleased]

### Added
- README: "Jama al Día" section (qué es, fuentes, cómo funciona, limitaciones) for the submission form.
- `jama_snapshot.yml`: optional `workflow_dispatch` input `origen` shown in the run name ("Jama snapshot (cron-job.org)"); scheduled runs show "schedule".
- "Jama al Día": `canal_desde: 2026-11-15`; Chile card with a fresh check but an official parte older than 24 h says "Sin parte nuevo" / "Último parte oficial (09/11 08:00): Abierto" / "Chile no actualiza este parte desde el 09/11…" (still amber; same wording in Telegram); administrative closures as one line "No incluye 1 cierre administrativo (enero 2022)."; forecast note reduced to one line "Alto = dentro del 10 % más alto para esta época, según el mismo modelo."; Telegram posts in at most 4 lines (🟢/🔴/🟠/⚪/🟡 per side, "Fuente: Pasos Fronterizos (AR) · MOP (CL). No es un canal oficial.", link), without the resolution line or the official-report time.
- "Jama al Día" round 2: "desde las HH:MM" (< 1 h) / "desde hace N h" / "desde el dd/mm" (> 24 h); durations as median and p75 ("La mitad… 3 de cada 4…"), no range; every history block states its base ("Sobre 67 cierres de Jama en el catálogo, 2016–2026"); /traccion with "Contamos desde" (`jama_al_dia.canal_desde`), a daily series per counter (subscriber counts per day in `telegram_estado.json`), "— todavía sin dato" for missing values and the channel/form buttons.
- "Jama al Día": channel (https://t.me/jamaaldia) and Plan Flotas form links and the waitlist number in `config.yaml`; `jama_snapshot.yml` skips the source requests (page rebuild only) when the last successful snapshot is under 20 min old, for a second hourly trigger (external `workflow_dispatch` at :47).
- "Jama al Día" review: Telegram and fleet CTAs under the status and in the footer; "Cerrado por horario" (grey, clock, "Abre a las HH:MM") and "fuera de horario" in the grid; stale sides (last check > 2 h or official report > 24 h) turn amber "Estado no confirmado"; header "Datos de las HH:MM"; relative dates; chart by month of the year + per-year line; plain-language forecast with the method in "Cómo se calcula".
- "Jama al Día" data fixes: "SIN DATO RECIENTE" when a side's last snapshot is older than 2 h (never posted to Telegram) and both page/last-consulted times in the header; "CERRADO POR HORARIO (abre HH:MM)" as its own grey state on the card and the 7-day grid; "último parte oficial hace N días" when the source's own report is older than 24 h; monthly chart counts only total/partial closures without `confianza=baja`, stacked nieve vs otros (67 of 110); durations say "1 día", leave administrative closures out of the median; `assets/jama/cierres.json` gains `confianza`, `administrativo`, `url_inicio`, `url_reapertura`.
- `reports/`: coverage, precision, manual review and validation regenerated with rules v4 (`PARSER_VERSION` 6) on the full backfill (4,570 articles, 578 events).
- "Jama al Día": `corredor jama-pagina` (static GitHub Pages site: AR/CL status with "desde hace X h", 7-day hourly blocks, monthly closures 2016–2026 and closure durations from `assets/jama/cierres.json`, 72 h snowfall sum and max wind gust vs 72 h sums/maxima of the forecast model's own climatology (from 2021; higher of Jama / CH-27 shown; banner only if both "alto") (`wind_gusts_10m`, optional `variables` in `OpenMeteoClient.forecast`/`historical_forecast`, separate cache folders), `/traccion`), `corredor jama-cierres`, `corredor jama-telegram` (posts only on a combined-state change plus an 08:00 summary; state in `data-snapshots`), `jama_al_dia` in `config.yaml`; `jama_snapshot.yml` now runs hourly and deploys Pages.
- Dashboard: weather-only points (`solo_clima`, e.g. `ch27_alto`) are left out of the map, the point list and the forecast download.
- `make tablero`: offline dashboard data layer in `tablero/dist/` (single `index.html`, bare
  unstyled views until the design brief, SVG map from `assets/geo`, no external resources, CSP
  with hashes, service worker, geolocation → nearest critical point; events read through
  `ClosureEvent`). Forecast risk as a percentile of the
  forecast model's own climatology (Historical Forecast API, #26); `umbrales_elegidos` in
  `config.yaml` (empty → "Umbral pendiente de definición"); `docs/USO.md`.
- `docs/FUENTES.md`: control misses expected from outlets we do not collect.
- `corredor recolectar --paralelo` (one queue per host), `--max-solicitudes` (0 = no cap), a
  listing pass with `--completo` (`recoleccion/<id>.plan.json`: sitemap URLs, slug-filter
  candidates, estimated time) and `SourceBlocked` to stop one source on 403/429 storms or
  pages without metadata.

### Changed
- `AGENTS.md`: the git identity rule no longer requires Emiliano Flores as commit author; author and committer emails must still end in `@users.noreply.github.com` (same as the `identity-guard` hook).
- Rules extractor (`PARSER_VERSION` 6): a suggested alternate route is not a closure of
  that route; an accented "cerró" no longer drops a per-route event; cut + protest actor
  (comunidades, vecinos, gremio…) → `protesta`; Jama closed by unspecified weather → `nieve`
  with `confianza=baja` only May–September; accident/freight `otro` stories without a
  closure term are dropped. Dedup: point-less merges and absorptions need the same cause
  family.
- Rules extractor (`PARSER_VERSION` 5): articles naming several routes and no place give one
  event per route, each with the cause and kind of its own clause; "N.º 9" route prefix;
  "mano única"/"paso alternado" are partial. Dedup: ties go to the event with more mentions;
  events whose only sources republish get `confianza=baja` and a note.
- `make precision`: labels whose catalog value changed since labelling become `revisar`
  (listed old → new) and, like `nd`, are left out of precision; `ok_corte` "ok" counts as si.
- `make cobertura` reports optimistic and strict coverage (strict: a point-less event does
  not cover a control event with a place).
- `clima.reserva_pronostico`: calls archive downloads leave for the forecast build.
- `SCHEMA_VERSION` 2 → 3: `eventos.fecha_inicio`, `eventos.fecha_fin`, `eventos.lado`
  (AR/CL/ambos/desconocido, Paso de Jama only) and `puntos.solo_clima`.
- Rules extractor (`PARSER_VERSION` 4): one event per critical point named in the article;
  RN 9 scope starts at Yala (new points `rn9_yala_lozano`, `rn9_leon`; south of Yala dropped;
  Yala–León accidents only with a total closure); Jama side from the text, Chilean-side
  closures are `total`; wind without snow → `otro` with note `viento`; "camino a Jama" is a
  destination, not the place; Saladillo → `rn52_ronqui_angosto`.
- Dedup: one point per event; point-less mentions merge by route, ±2 days and cause family
  (aluvión + crecida); follow-ups (habilitan, reabren, sigue cortada, horarios, trabajos…)
  extend a closure up to 7 days and inherit its cause; events carry `fecha_inicio`/`fecha_fin`.
- Weather-only point `ch27_alto` (Ruta CH-27 high section, OSM way/53264481) and
  `validacion.md` snow at Jama by side (AR/ambos, CL, combined).
- `make cobertura`: coverage against the owner's control list in `reports/control/`
  (not loaded into the pipeline).
- Manual review: `ok_corte` (si/no/fuera) column; `precision.md` reports the `ok_corte` rate and
  field precision on `ok_corte = si` rows only; the owner's first labels carried over by URL
  (`revision_manual_v1.csv` kept) and `revision_manual_completar.csv` completes the strata.

### Changed
- Rules extractor (`PARSER_VERSION` 3): drug seizures / Gendarmería operations need a closure
  term next to a road word; health/administrative border closures (Covid…) get `causa=otro`
  with a note. `revision_manual.csv` is a stratified sample with `estrato`; `precision.md`
  reports per field and stratum with n; `validacion.md` adds the merged `lluvia` variant,
  n per value and "muestra chica". Sitemap filter C is kept (owner decision).
- Rules extractor (`PARSER_VERSION` 2): a closure term must refer to the road (`is_road_closure`), which drops
  service cuts, train and mine closures; first real-data `calidad_catalogo.md`,
  `revision_manual.csv` and `validacion.md`; only enabled sources count as stable.
- `SCHEMA_VERSION` 1 → 2 (`puntos.osm`, `puntos.nota_geo`, #25). Existing DuckDB tables
  get missing model columns added before any write.
- `make datos` runs `recolectar`, `clima`, fetches the `data-snapshots` Jama JSONL and
  then `corredor datos`.
- `clima.max_llamadas_diarias` in `config.yaml` 500 → 1500 (owner's decision) to finish
  the 2016→today archive for all 13 points in one day; the code default stays 500.
- Jama snapshots store only allowlisted status/schedule/timestamp fields per source; other
  fields (e.g. MOP `CREATEDBY`/`RESPONSABLE` operator usernames) are dropped and only their
  names are logged. `JamaCollector.PARSER_VERSION` 1 → 2.
- AGENTS.md rule 2: documented public APIs whose terms allow programmatic use (currently
  Open-Meteo) may skip only the robots.txt check, host by host via `robots_exempt_hosts`,
  with an ADR and the owner's approval.
- `jujuyaldia` moved from the WordPress API (its robots.txt disallows `/wp-json/`) to
  `SitemapSource` over its allowed `wp-sitemap.xml` index. 404 cache TTL
  (`http.not_found_ttl_h`) lowered from 24 h to 1 h.
- docs/FUENTES.md: robots.txt column rechecked for all candidates with the production
  parser (all `User-agent: *` groups combined).

### Added
- "Jama al Día": `canal_desde: 2026-11-15`; Chile card with a fresh check but an official parte older than 24 h says "Sin parte nuevo" / "Último parte oficial (09/11 08:00): Abierto" / "Chile no actualiza este parte desde el 09/11…" (still amber; same wording in Telegram); administrative closures as one line "No incluye 1 cierre administrativo (enero 2022)."; forecast note without the "Alto" sentence.
- "Jama al Día" round 2: "desde las HH:MM" (< 1 h) / "desde hace N h" / "desde el dd/mm" (> 24 h); durations as median and p75 ("La mitad… 3 de cada 4…"), no range; every history block states its base ("Sobre 67 cierres de Jama en el catálogo, 2016–2026"); /traccion with "Contamos desde" (`jama_al_dia.canal_desde`), a daily series per counter (subscriber counts per day in `telegram_estado.json`), "— todavía sin dato" for missing values and the channel/form buttons.
- Integration: `RuleBasedExtractor`, `EventDeduplicator` (±2 days, point or headline
  Jaccard), optional `LLMExtractor` (validated, cached, not wired to a provider),
  `ThresholdCalibrator` (absolute and per-cell seasonal percentile candidates) and the
  `datos`, `reporte`, `calibrar`, `precision` commands writing `eventos`, Parquet exports,
  `reports/calidad_catalogo.md`, `revision_manual.csv`, `validacion.md`, `precision.md`.
- `OpenMeteoClient.historical_forecast(point, start, end, model)`: hourly series from the
  Historical Forecast API for a given forecast model, cached under
  `data/clima/pronostico_historico/` (no downloads yet; for day 2, #26).
- `SitemapSource` `params.sitemap_indice`/`sitemap_hijos`: paginated sitemap indexes
  (children chosen per month by `lastmod`, URLs filtered by their date).
- Generic sources `WordPressApiSource`, `SitemapSource` and `RssSource` (yearly WP windows,
  monthly sitemaps with slug filter C, resumable checkpoints that tell empty from error,
  per-run request cap), `corredor recolectar` CLI, trimmed fixtures and per-outlet smoke tests.
- Repository foundation: uv project (Python 3.11), typed models (`SCHEMA_VERSION = 1`),
  `config.yaml` with provisional critical points and the approved source survey,
  `PoliteFetcher` (robots.txt RFC 9309, Crawl-delay, rate limit, retries, disk cache),
  shared extraction regexes, DuckDB repository, lineage manifest and `corredor` CLI.
- Tooling: Makefile, pre-commit (identity guard, ruff, mypy, detect-secrets), docs guard,
  two-step release (`make release` opens a release PR, `make tag` pushes the tag), CI and
  release workflows, Dependabot, PR and issue templates. CodeQL (Python + Actions) runs via
  GitHub default setup.
- Geo: `corredor geo` / `make geo` builds RN 9, RN 52 and the Tren Solar line from OSM via
  Overpass (`OverpassClient` with mirror fallback, `OverpassExporter`), writes committed
  GeoJSON with ODbL attribution under `assets/geo/` and `reports/geo_verificacion.md`;
  `CriticalPointRegistry.verify` derives coordinates, km and sources from each point's OSM
  object; `NominatimGeocoder` (robots-bound). `CriticalPoint` gains `osm` and `nota_geo`;
  12 of 13 points verified in `config.yaml`.
- Weather (Child D): `OpenMeteoClient` (archive `era5_seamless` 2016→today in one request
  per point, forecast, grid cell and elevation per point, weighted daily call cap
  `clima.max_llamadas_diarias` = 500, Parquet cache by lat/lon/range), antecedent
  features (24/48/72 h, 7 d, max hourly, snow), `corredor clima` / `make clima` loading
  `clima_diario`, and `reports/clima_grilla.md`.
- `PoliteFetcher`: `http.robots_exempt_hosts` skips only the robots.txt check for the 3
  exact Open-Meteo API hosts (ADR 0002); everything else unchanged.
- Docs: README (es-AR), AGENTS.md, CONTRIBUTING.md, FUENTES.md, SCRAPING.md, DATOS.md,
  ADR 0001 and playbooks.
- Paso de Jama snapshots: `corredor snapshot-jama` (collectors for Vialidad MOP Chile
  ArcGIS and argentina.gob.ar, one request each, failures recorded as `error` lines) and
  the `jama_snapshot.yml` workflow that appends to `snapshots/jama_estado.jsonl` on the
  `data-snapshots` branch every 3 h. `PoliteFetcher.get` gains `refresh=True`.
- Custom news sources: `VialidadNacionalSource` (national news listing filtered to Jujuy /
  RN 52 / corridor places) and `ElTribunoSource` (El Tribuno de Jujuy tag pages), registered
  in `CUSTOM_CLASSES` and enabled in `config.yaml`. Listing metadata only.
