#!/usr/bin/env python3
"""Minimal helpers for the unofficial FPL API."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

BASE = "https://fantasy.premierleague.com/api/"
UA = "Mozilla/5.0 (compatible; fpl-api-docs/1.0)"


def get_json(path: str, **query: Any) -> Any:
    """GET /api/{path} and return parsed JSON.

    path examples:
        "bootstrap-static/"
        "fixtures/"
        "element-summary/1/"
        "entry/1/history/"
    """
    url = BASE + path.lstrip("/")
    if query:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(
            {k: v for k, v in query.items() if v is not None}
        )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def current_event(bootstrap: dict | None = None) -> dict:
    bootstrap = bootstrap or get_json("bootstrap-static/")
    for event in bootstrap["events"]:
        if event.get("is_current"):
            return event
    for event in bootstrap["events"]:
        if event.get("is_next"):
            return event
    return bootstrap["events"][0]


def player_by_web_name(name: str, bootstrap: dict | None = None) -> dict | None:
    bootstrap = bootstrap or get_json("bootstrap-static/")
    needle = name.strip().lower()
    for player in bootstrap["elements"]:
        if player["web_name"].lower() == needle:
            return player
    return None


if __name__ == "__main__":
    data = get_json("bootstrap-static/")
    gw = current_event(data)
    print(f"Managers: {data['total_players']:,}")
    print(f"Players:  {len(data['elements'])}")
    print(f"Current:  {gw['name']}  deadline={gw['deadline_time']}  finished={gw['finished']}")
    fixtures = get_json("fixtures/", event=gw["id"])
    print(f"Fixtures in {gw['name']}: {len(fixtures)}")
