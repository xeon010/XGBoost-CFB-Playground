import joblib
import pandas as pd

# === Load trained model ===
model = joblib.load("../data/models/score_diff_model.joblib")

# === Load new games ===
new_games = pd.read_csv("../data/input/new_games.csv")

# === Match the model’s feature set ===
# Your training data had: elo_diff, is_neutral
features = ["elo_diff", "is_neutral"]
X_new = new_games[features]

# === Predict score difference ===
new_games["pred_score_diff"] = model.predict(X_new)

# === Derive predicted scores (simple heuristic) ===
new_games["pred_home_points"] = 28 + (new_games["pred_score_diff"] / 2)
new_games["pred_away_points"] = 28 - (new_games["pred_score_diff"] / 2)

# === Predicted winner ===
new_games["predicted_winner"] = new_games.apply(
    lambda row: row["homeTeam"] if row["pred_score_diff"] > 0 else row["awayTeam"],
    axis=1
)

# === Display + save ===
print(new_games[[
    "homeTeam", "awayTeam",
    "predicted_winner",
    "pred_score_diff",
    "pred_home_points",
    "pred_away_points"
]])

new_games.to_csv("../data/output/predictions.csv", index=False)
print("\n✅ Predictions saved to ../data/predictions/predictions.csv")
