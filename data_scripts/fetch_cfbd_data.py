"""
Fetch historical college football data (games, ratings, lines, weather)
from CollegeFootballData.com API and save as CSVs.
"""

import requests
import pandas as pd
import os
import time

# ======== CONFIGURATION ======== #
API_KEY = os.getenv("CFBD_API_KEY")
if not API_KEY:
    raise ValueError("Missing CFBD_API_KEY environment variable.")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.collegefootballdata.com"

YEARS = range(2014, 2024)  # last 10 full seasons
SAVE_DIR = "data/raw"

os.makedirs(SAVE_DIR, exist_ok=True)
# =============================== #


def fetch_cfbd(endpoint, params=None, delay=1):
    """Make a GET request to the CFBD API."""
    url = f"{BASE_URL}{endpoint}"
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code != 200:
        print(f"[WARN] Failed ({r.status_code}): {url}")
        return []
    time.sleep(delay)  # to avoid hammering the API
    return r.json()


def fetch_games():
    """Fetch all games by year."""
    all_games = []
    for year in YEARS:
        print(f"Fetching games for {year}...")
        data = fetch_cfbd("/games", params={"year": year})
        all_games.extend(data)
    pd.DataFrame(all_games).to_csv(f"{SAVE_DIR}/games.csv", index=False)
    print(f"✅ Saved games.csv ({len(all_games)} rows)")


def fetch_elo():
    """Fetch team Elo ratings by year."""
    all_elo = []
    for year in YEARS:
        print(f"Fetching Elo ratings for {year}...")
        data = fetch_cfbd("/ratings/elo", params={"year": year})
        for d in data:
            d["year"] = year
        all_elo.extend(data)
    pd.DataFrame(all_elo).to_csv(f"{SAVE_DIR}/elo.csv", index=False)
    print(f"✅ Saved elo.csv ({len(all_elo)} rows)")


def fetch_lines():
    """Fetch betting lines by year."""
    all_lines = []
    for year in YEARS:
        print(f"Fetching betting lines for {year}...")
        data = fetch_cfbd("/lines", params={"year": year})
        all_lines.extend(data)
    pd.DataFrame(all_lines).to_csv(f"{SAVE_DIR}/lines.csv", index=False)
    print(f"✅ Saved lines.csv ({len(all_lines)} rows)")


if __name__ == "__main__":
    print("=== Starting CFBD Data Download ===")
    fetch_games()
    fetch_elo()
    fetch_lines()
    print("🎉 All data downloaded and saved in data/raw/")
