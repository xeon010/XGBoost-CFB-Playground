import joblib
from xgboost import XGBRegressor
import pandas as pd

# Load and train your model (example)
df = pd.read_csv("data/processed/games_master.csv")
features = ["elo_diff", "is_neutral"]
target = "score_diff"

X = df[features]
y = df[target]

model = XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05)
model.fit(X, y)

# Save to disk
joblib.dump(model, "data/models/score_diff_model.joblib")
print("Model saved!")
