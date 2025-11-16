"""
Clean and combine College Football Data CSVs (games, elo, lines)
into one ML-ready dataset.
"""

import pandas as pd
import os

RAW_DIR = "data/raw"
OUT_DIR = "data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

# === 1. Load the raw files ===
games = pd.read_csv(f"{RAW_DIR}/games.csv")
elo = pd.read_csv(f"{RAW_DIR}/elo.csv")
lines = pd.read_csv(f"{RAW_DIR}/lines.csv")

# === 2. Basic cleaning ===
# Keep essential fields
games = games[
    [
        "id",
        "season",
        "week",
        "homeTeam",
        "awayTeam",
        "homePoints",
        "awayPoints",
        "venueId",
    ]
]

# Drop games with no score
games = games.dropna(subset=["homePoints", "awayPoints"])

# Create target variable (1 = home win, 0 = home loss)
games["home_win"] = (games["homePoints"] > games["awayPoints"]).astype(int)

# --- Clean Elo ---
elo = elo.rename(columns={"year": "season"})
elo_home = elo.rename(columns={"team": "homeTeam", "elo": "home_elo"})
elo_away = elo.rename(columns={"team": "awayTeam", "elo": "away_elo"})

# Merge Elo ratings
games = games.merge(elo_home[["homeTeam","season","home_elo"]], on=["homeTeam","season"], how="left")
games = games.merge(elo_away[["awayTeam","season","away_elo"]], on=["awayTeam","season"], how="left")

# Feature engineering
games["elo_diff"] = games["home_elo"] - games["away_elo"]
games["score_diff"] = games["homePoints"] - games["awayPoints"]
games["is_neutral"] = (games["venueId"] == 0).astype(int)

# Drop rows missing Elo
games = games.dropna(subset=["home_elo", "away_elo"])

# === 6. Save clean dataset ===
out_path = f"{OUT_DIR}/games_master.csv"
games.to_csv(out_path, index=False)

print(f"✅ Cleaned dataset saved to {out_path}")
print(f"Rows: {len(games)} | Columns: {len(games.columns)}")
