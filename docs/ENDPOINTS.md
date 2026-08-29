# FPL API — complete endpoint notes

Base: `https://fantasy.premierleague.com/api/`

Verified 29 August 2026. Current event at that time: **GW2**. Previous: GW1. Next: GW3 (deadline 2026-09-04T17:30:00Z).

---

## 1. `GET /bootstrap-static/`

The one payload most tools need. ~1.6 MB.

### Top-level keys

| Key | Shape | Notes |
|---|---|---|
| `chips` | array | Two of each chip. `start_event` / `stop_event` define the window. `chip_type` is `transfer` or scoring override. |
| `events` | array[38] | Deadlines, `is_current` / `is_next` / `is_previous`, `finished`, averages, chip plays |
| `game_settings` | object | Squad size, budget, transfer cap, sell-on fee, cup + league limits |
| `game_config` | object | `settings`, `rules`, `scoring` |
| `phases` | array | Monthly ranking windows (`Overall`, `August`…`May`) |
| `teams` | array[20] | Strength overall / attack / defence, home and away |
| `total_players` | int | Registered managers |
| `element_stats` | array | Stat name catalogue |
| `element_types` | array | GKP=2, DEF=5, MID=5, FWD=3 `squad_select` |
| `elements` | array | Every player (~622 in 2026/27, 109 fields) |

### Useful `elements[]` fields

**Identity:** `id`, `web_name`, `first_name`, `second_name`, `known_name`, `photo`, `team`, `team_code`, `element_type`, `squad_number`, `opta_code`, `birth_date`, `region`

**Price / ownership:** `now_cost`, `cost_change_event`, `cost_change_start`, `selected_by_percent`, `transfers_in`, `transfers_out`, `transfers_in_event`, `transfers_out_event`, `value_form`, `value_season`, `now_cost_rank`

**Form / projections:** `form`, `points_per_game`, `total_points`, `event_points`, `ep_this`, `ep_next`

**Availability:** `status` (`a` available, `d` doubtful, `i` injured, `s` suspended, `u` unavailable), `chance_of_playing_this_round`, `chance_of_playing_next_round`, `news`, `news_added`, `can_select`, `can_transact`, `removed`

**Classic stats:** `minutes`, `starts`, `goals_scored`, `assists`, `clean_sheets`, `goals_conceded`, `own_goals`, `penalties_saved`, `penalties_missed`, `yellow_cards`, `red_cards`, `saves`, `bonus`, `bps` (+ several `*_per_90`)

**ICT:** `influence`, `creativity`, `threat`, `ict_index` + ranks

**Expected:** `expected_goals`, `expected_assists`, `expected_goal_involvements`, `expected_goals_conceded` (+ per 90)

**DEFCON (2025/26+):** `defensive_contribution`, `defensive_contribution_per_90`, `clearances_blocks_interceptions`, `recoveries`, `tackles`

**Set pieces:** `penalties_order`, `direct_freekicks_order`, `corners_and_indirect_freekicks_order` (+ text fields)

**Price movement helpers:** `price_change_percent`, `price_change_hourly_rate`, `price_change_projections`, `price_change_locked_until`, `price_change_calibrating`

### Thin aliases

- `GET /elements/` — just the player array
- `GET /events/` — just the gameweek array

`GET /teams/` is **404**. Teams only come from bootstrap.

---

## 2. Fixtures

### `GET /fixtures/`
### `GET /fixtures/?event={gw}`
### `GET /fixtures/?future=1`

Array of fixture objects.

| Field | Meaning |
|---|---|
| `id`, `code`, `pulse_id` | Identifiers |
| `event` | Gameweek number (null if unscheduled) |
| `kickoff_time` | ISO UTC |
| `team_h`, `team_a` | Club ids |
| `team_h_score`, `team_a_score` | Null until played |
| `finished`, `finished_provisional`, `started`, `minutes` | State |
| `team_h_difficulty`, `team_a_difficulty` | FDR 1–5 |
| `stats` | Goals, assists, own goals, pens, cards, saves, bonus, BPS when available |

---

## 3. Player detail

### `GET /element-summary/{element_id}/`

| Key | Contents |
|---|---|
| `fixtures` | Remaining fixtures with difficulty, kickoff, `is_home` |
| `history` | This season, one row per finished GW |
| `history_past` | Previous-season totals |

Use this for multi-GW projections and minutes-risk.

---

## 4. Live gameweek

### `GET /event/{event_id}/live/`

```json
{ "elements": [ { "id": 1, "stats": { "...": "..." }, "explain": [ ] } ] }
```

`stats` mirrors the classic scoring fields for that GW. `explain` is the points breakdown the official UI shows.

### `GET /event-status/`

```json
{ "status": [ { "bonus_added": true, "date": "...", "event": 2, "points": "r" } ], "leagues": "Updating" }
```

### `GET /dream-team/` and `GET /dream-team/{event_id}/`

```json
{ "top_player": { "id": 0, "points": 0 }, "team": [ ] }
```

Empty-ish early season until published.

---

## 5. Public manager (`entry`)

### `GET /entry/{entry_id}/`

Profile: name, overall/event points and rank, favourite team, region, years active, leagues (classic / h2h / cup), last-deadline bank and value.

### `GET /entry/{entry_id}/history/`

- `current[]` — per GW: points, rank, bank, value, `event_transfers`, `event_transfers_cost`, `points_on_bench`
- `past[]` — previous seasons
- `chips[]` — chips played this season

### `GET /entry/{entry_id}/transfers/`

Array of `{ element_in, element_out, entry, event, time, cost }`. Empty `[]` if none.

### `GET /entry/{entry_id}/event/{event_id}/picks/`

```json
{
  "active_chip": null,
  "automatic_subs": [],
  "entry_history": {},
  "picks": [
    {
      "element": 123,
      "position": 1,
      "multiplier": 1,
      "is_captain": false,
      "is_vice_captain": false
    }
  ]
}
```

Positions 1–11 are the XI; 12–15 are the bench in auto-sub order. Captain `multiplier` is 2 (or 3 on Triple Captain). Returns 404 if that manager has no locked squad for the event.

### Dead

- `GET /entry/{id}/cup/` → 404
- `GET /entry/{id}/event/{gw}/` (no `picks`) → 404

---

## 6. Leagues and cups

### `GET /leagues-classic/{league_id}/standings/`

Query params:

- `page_standings` (default 1)
- `page_new_entries`
- `phase` (1 = Overall; see bootstrap `phases`)

Response keys: `league`, `standings`, `new_entries`, `last_updated_data`.

`GET /leagues-classic/{id}/` without `/standings/` is **403**.

### `GET /league/{league_id}/cup-status/`

Qualifying league, method, draw type, qualification event and numbers.

### H2H

These paths exist in older wrappers but returned **404** when probed with dummy ids on 29 Aug 2026:

- `/leagues-h2h-standings/{id}/`
- `/leagues-h2h-matches/league/{id}/`
- `/leagues-h2h/{id}/standings/`

Treat H2H as optional and probe the real league id before building UI on it.

---

## 7. Authenticated

Need the session cookie from a logged-in browser on fantasy.premierleague.com (`pl_profile` / related cookies). Do not commit cookies.

| Path | Unauthenticated result | Authenticated purpose |
|---|---|---|
| `/me/` | Tiny `{ "player": null, "watched": [] }` | Current user + watched players |
| `/my-team/{entry_id}/` | 403 | Picks, chips, transfers remaining, bank |
| `/entry/{id}/transfers-latest/` | 403 | Transfers staged this GW |
| `POST /transfers/` | 403 | Confirm transfers |

For personal tools, pasting the 15 names + bank + free transfers is simpler than shipping login.

---

## 8. Misc

| Path | Shape |
|---|---|
| `/regions/` | 255 `{ id, name, code, iso_code_short, iso_code_long }` |
| `/team/set-piece-notes/` | `{ last_updated, teams: [...] }` |
| `/stats/most-valuable-teams/` | Top 10 `{ entry, name, player_name, value_with_bank, total_transfers }` |
| `/stats/best-classic-private-leagues/` | Top 10 `{ league, entries, average_score, name }` |

`GET /stats/` (no suffix) is 404.

---

## 9. Game settings worth knowing

From `bootstrap-static.game_settings` in 2026/27:

- `squad_squadsize` 15, `squad_team_limit` 3, `squad_total_spend` 1000 (£100.0m)
- `transfers_cap` 20 per GW (ignored on WC / FH)
- `max_extra_free_transfers` 5 stored
- `transfers_sell_on_fee` 0.5
- Cup start / stop event ids and qualifying method
- H2H points for win / draw / loss and league size caps

Scoring detail (appearance, goals, DEFCON thresholds, BPS) is under `game_config.scoring` plus the official rules page.

---

## 10. Suggested client flow

1. Fetch `/bootstrap-static/` once and cache.
2. Read `events` to find `is_current` / `is_next` and the deadline.
3. Fetch `/fixtures/?future=1` for FDR.
4. For a named player, map `web_name` → `id`, then `/element-summary/{id}/`.
5. After deadline, `/entry/{id}/event/{gw}/picks/` for locked squads.
6. During matches, poll `/event/{gw}/live/` + `/event-status/` slowly.
7. For mini-leagues, page `/leagues-classic/{id}/standings/`.
