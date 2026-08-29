# Unofficial Fantasy Premier League API

Live-verified endpoint catalogue for the **2026/27** season.

> There is no official public FPL API spec. This repo documents the JSON endpoints the official site uses at `https://fantasy.premierleague.com/api/`.
>
> Last probed: **29 August 2026** (GW2 current). Status codes and payload shapes were checked with a normal browser User-Agent.

## Quick start

```bash
curl -sA "Mozilla/5.0" https://fantasy.premierleague.com/api/bootstrap-static/ | python3 -m json.tool | head
```

Python:

```python
from examples.quickstart import get_json

data = get_json("bootstrap-static/")
print(data["total_players"], "managers")
print(len(data["elements"]), "players")
```

Or run the probe that re-checks every known path:

```bash
python3 examples/probe.py
```

## Base URL

```
https://fantasy.premierleague.com/api/
```

Most endpoints are unauthenticated `GET`s. Private team endpoints need a logged-in session cookie from fantasy.premierleague.com and return **403** without it.

## Endpoint map

| Auth | Method | Path | Status (29 Aug 2026) | Purpose |
|---|---|---|---|---|
| Public | GET | `/bootstrap-static/` | 200 | Core payload: players, teams, events, chips, rules |
| Public | GET | `/elements/` | 200 | Player list only (same objects as bootstrap `elements`) |
| Public | GET | `/events/` | 200 | Gameweek list only |
| Public | GET | `/fixtures/` | 200 | All 380 fixtures |
| Public | GET | `/fixtures/?event={gw}` | 200 | Fixtures for one gameweek |
| Public | GET | `/fixtures/?future=1` | 200 | Remaining fixtures |
| Public | GET | `/element-summary/{element_id}/` | 200 | Player fixtures + GW history + past seasons |
| Public | GET | `/event/{event_id}/live/` | 200 | Live GW points and explain breakdown |
| Public | GET | `/event-status/` | 200 | Bonus / league processing flags |
| Public | GET | `/dream-team/` | 200 | Season-to-date official dream team |
| Public | GET | `/dream-team/{event_id}/` | 200 | Dream team for a gameweek |
| Public | GET | `/entry/{entry_id}/` | 200 | Public manager profile |
| Public | GET | `/entry/{entry_id}/history/` | 200 | Per-GW history, past seasons, chips used |
| Public | GET | `/entry/{entry_id}/transfers/` | 200 | Transfer log |
| Public | GET | `/entry/{entry_id}/event/{gw}/picks/` | 200 | Locked 15-man squad for a GW |
| Public | GET | `/leagues-classic/{league_id}/standings/` | 200 | Classic league table (`page_standings`, `page_new_entries`, `phase`) |
| Public | GET | `/league/{league_id}/cup-status/` | 200 | League cup qualification |
| Public | GET | `/regions/` | 200 | Registration countries |
| Public | GET | `/team/set-piece-notes/` | 200 | Official set-piece taker notes |
| Public | GET | `/stats/most-valuable-teams/` | 200 | Most valuable squads |
| Public | GET | `/stats/best-classic-private-leagues/` | 200 | Top private classic leagues |
| Cookie | GET | `/me/` | 200 stub / auth for full | Current user |
| Cookie | GET | `/my-team/{entry_id}/` | 403 unauth | Live squad, bank, free transfers, chips |
| Cookie | GET | `/entry/{entry_id}/transfers-latest/` | 403 unauth | Unconfirmed transfers this GW |
| Cookie | POST | `/transfers/` | 403 unauth | Submit transfers |
| Dead | GET | `/bootstrap-dynamic/` | 404 | Removed |
| Dead | GET | `/entry/{id}/cup/` | 404 | Cup now lives on entry + cup-status |
| Fragile | GET | `/leagues-h2h-…` | 404 often | H2H routes exist in old clients, unreliable |

Full field notes: [docs/ENDPOINTS.md](docs/ENDPOINTS.md)  
Machine-readable catalogue: [data/endpoints.json](data/endpoints.json)

## What you can build

| Goal | Endpoints |
|---|---|
| Prices, ownership, form, injuries, xP | `/bootstrap-static/` |
| Fixture difficulty / blanks / doubles | `/fixtures/` + bootstrap `events` |
| Player form charts and remaining run | `/element-summary/{id}/` |
| Live scores and bonus | `/event/{gw}/live/` + `/event-status/` |
| Anyone's public team | `/entry/{id}/event/{gw}/picks/` |
| Mini-league table | `/leagues-classic/{id}/standings/` |
| Rival history and hits | `/entry/{id}/history/` + `/transfers/` |
| Set-piece roles | `/team/set-piece-notes/` + player `*_order` fields |
| Price-change watch | bootstrap `transfers_*_event` + `price_change_*` |
| Your bank / free transfers | `/my-team/{id}/` (auth) or paste the squad |

## IDs and units

- **Player** = `element` id
- **Manager** = `entry` id (from `fantasy.premierleague.com/entry/{id}/`)
- **Club** = `team` id (1–20)
- **Gameweek** = `event` id (1–38)
- **Price** = `now_cost / 10` million pounds (`75` → £7.5m)
- Selling price = purchase price + half of any rise, floored to £0.1m

## Practical rules

- Send a browser `User-Agent`. Some paths 403 a bare Python/curl UA.
- Cache `/bootstrap-static/` — it is ~1.6 MB. Refetch after midnight UK (price changes) or before recommendations.
- Browser JS from another origin is blocked by CORS. Call the API from a server, Netlify function, or local script.
- No official rate limit is published. Do not hammer `/event/{gw}/live/` during matches.
- `/leagues-classic/{id}/` (no `/standings/`) returns 403. Always use the standings path.
- This is unofficial and can change without notice. Re-run `examples/probe.py` after a season rollover.

## Repo layout

```
README.md
LICENSE
docs/ENDPOINTS.md
data/endpoints.json
examples/quickstart.py
examples/probe.py
```

## Disclaimer

Not affiliated with the Premier League or Fantasy Premier League. Endpoints are reverse-engineered from the public website and may break. Do not use authenticated write endpoints against anyone else's team.

## Related

- [mcclowes/fpl-oas](https://github.com/mcclowes/fpl-oas) — unofficial OpenAPI spec
- Official site: [fantasy.premierleague.com](https://fantasy.premierleague.com)
