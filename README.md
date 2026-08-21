# NFL odds input

This public repository is the phone-editable input for the local NFL Betting Tool.
It contains odds only—never predictions, results, or the application's private SQLite
history.

## Edit from a phone

1. Open [`odds/current_odds.csv`](odds/current_odds.csv) on GitHub and tap the pencil.
2. Enter `away_moneyline`, `home_moneyline`, and `home_spread` for every game.
3. Use one identical `sportsbook` on every row.
4. Set every `snapshot_label` to exactly one of:
   - `Tuesday Opening`
   - `Friday Update`
   - `Pregame Closing`
5. Commit the change. A clear message such as `Week 1 Friday odds` is best.
6. In the NFL Betting Tool, select the same season/week and tap **Reload GitHub CSV**.

For `Pregame Closing`, keep only the games about to start. Use separate commits for the
Thursday, Sunday, and Monday batches. The app records the exact source commit and will
not allow an official closing prediction to be replaced.

## CSV contract

The header must remain:

```csv
season,week,snapshot_label,sportsbook,game_id,away_team,home_team,away_moneyline,home_moneyline,home_spread
```

Rules:

- Tuesday and Friday files need one row for every game in the selected NFL week.
- A `Pregame Closing` file may contain only the game or games about to start.
- No file may contain extra or duplicate game rows.
- One season, week, snapshot label, and sportsbook per file.
- American moneylines must include the sign when positive, such as `+150`; negative
  lines look like `-175`.
- `home_spread` uses normal sportsbook notation. A home favorite by 3.5 is `-3.5`; a
  home underdog by 3.5 is `+3.5`.
- Do not change `game_id`, `away_team`, or `home_team` after the weekly file is prepared.
- Blank or invalid odds cause the app to reject the entire file.

The raw URL used by the app is:

```text
https://raw.githubusercontent.com/meverhart913/nfl-odds-input/main/odds/current_odds.csv
```

## Weekly preparation

The `Prepare weekly odds file` GitHub Action runs Tuesday morning and replaces the file
with the next unplayed week's schedule and blank odds. It keeps the prior sportsbook
name when possible. It can also be run manually from the Actions tab.

Git history preserves every published version of the CSV. The local application's
saved snapshot—not this repository—is the official record of a prediction.
