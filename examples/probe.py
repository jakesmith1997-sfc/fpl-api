#!/usr/bin/env python3
"""Re-check known FPL API paths and print status / payload shape."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

BASE = "https://fantasy.premierleague.com/api/"
UA = "Mozilla/5.0 (compatible; fpl-api-docs/1.0)"

PATHS = [
    "bootstrap-static/",
    "elements/",
    "events/",
    "fixtures/",
    "fixtures/?event=1",
    "fixtures/?future=1",
    "event-status/",
    "regions/",
    "team/set-piece-notes/",
    "stats/most-valuable-teams/",
    "stats/best-classic-private-leagues/",
    "dream-team/",
    "dream-team/1/",
    "event/1/live/",
    "entry/1/",
    "entry/1/history/",
    "entry/1/transfers/",
    "entry/1/event/1/picks/",
    "entry/1/cup/",
    "leagues-classic/314/standings/",
    "league/314/cup-status/",
    "leagues-h2h-standings/1/",
    "leagues-h2h-matches/league/1/",
    "me/",
    "my-team/1/",
    "element-summary/1/",
    "bootstrap-dynamic/",
]


def probe(path: str) -> str:
    url = BASE + path
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            code = resp.status
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                return f"{code} {len(raw):7d}  {path}  (not json)"
            if isinstance(payload, dict):
                shape = "dict keys=" + ",".join(list(payload.keys())[:8])
            elif isinstance(payload, list):
                shape = f"list len={len(payload)}"
            else:
                shape = type(payload).__name__
            return f"{code} {len(raw):7d}  {path}  {shape}"
    except urllib.error.HTTPError as exc:
        return f"{exc.code}       -  {path}  {exc.reason}"
    except Exception as exc:  # noqa: BLE001
        return f"ERR       -  {path}  {exc}"


def main() -> None:
    print(f"Base {BASE}")
    for path in PATHS:
        print(probe(path))


if __name__ == "__main__":
    main()
