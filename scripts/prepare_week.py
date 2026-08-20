"""Prepare the next unplayed NFL week's phone-editable odds CSV."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


SCHEDULE_URL = "https://github.com/nflverse/nfldata/raw/master/data/games.csv"
OUTPUT = Path(__file__).resolve().parents[1] / "odds" / "current_odds.csv"
FIELDS = [
    "season",
    "week",
    "snapshot_label",
    "sportsbook",
    "game_id",
    "away_team",
    "home_team",
    "away_moneyline",
    "home_moneyline",
    "home_spread",
]


def previous_sportsbook() -> str:
    if not OUTPUT.exists():
        return "ENTER_SPORTSBOOK"
    with OUTPUT.open(newline="", encoding="utf-8") as handle:
        first = next(csv.DictReader(handle), None)
    if not first:
        return "ENTER_SPORTSBOOK"
    value = str(first.get("sportsbook", "")).strip()
    return value or "ENTER_SPORTSBOOK"


def download_schedule() -> list[dict[str, str]]:
    request = Request(SCHEDULE_URL, headers={"User-Agent": "nfl-odds-input/1.0"})
    with urlopen(request, timeout=60) as response:
        lines = (line.decode("utf-8") for line in response)
        return list(csv.DictReader(lines))


def choose_week(rows: list[dict[str, str]]) -> tuple[int, int, list[dict[str, str]]]:
    today = date.today().isoformat()
    future = [
        row
        for row in rows
        if row.get("gameday", "") >= today
        and row.get("game_type") in {"REG", "WC", "DIV", "CON", "SB"}
        and row.get("game_id")
    ]
    if not future:
        raise RuntimeError("No future NFL games were found in nflverse.")
    first = min(future, key=lambda row: (row["gameday"], row["game_id"]))
    season, week = int(first["season"]), int(first["week"])
    selected = [
        row
        for row in future
        if int(row["season"]) == season and int(row["week"]) == week
    ]
    return season, week, sorted(selected, key=lambda row: (row["gameday"], row["game_id"]))


def main() -> None:
    sportsbook = previous_sportsbook()
    season, week, games = choose_week(download_schedule())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for game in games:
            writer.writerow(
                {
                    "season": season,
                    "week": week,
                    "snapshot_label": "Tuesday Opening",
                    "sportsbook": sportsbook,
                    "game_id": game["game_id"],
                    "away_team": game["away_team"],
                    "home_team": game["home_team"],
                    "away_moneyline": "",
                    "home_moneyline": "",
                    "home_spread": "",
                }
            )
    print(f"Prepared {len(games)} games for season {season}, week {week}.")


if __name__ == "__main__":
    main()
