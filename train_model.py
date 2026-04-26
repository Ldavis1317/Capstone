import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
import joblib
print("SCRIPT STARTED")
# ================================
# LOAD DATA
# ================================
# Load your Statcast dataset (or whichever CSV you are using to train)
df = pd.read_csv("676979_data.csv")

print("Columns loaded successfully")

# ================================
# FEATURE SELECTION
# ================================

# Input features (what the model uses to predict)
numeric_features = [
    "release_speed",
    "release_spin_rate",
    "release_pos_x",
    "release_pos_y",
    "release_pos_z",
    "release_extension",
    "pfx_x",
    "pfx_z",
    "vx0",
    "vy0",
    "vz0",
    "ax",
    "ay",
    "az",
    "spin_axis"
]

categorical_feature = "pitch_type"

# Targets (what we are predicting)
target_x = "plate_x"
target_z = "plate_z"

# ================================
# CLEAN DATA
# ================================
# Keep only needed columns
keep_cols = numeric_features + [categorical_feature, target_x, target_z]
df = df[keep_cols]

# Drop rows with missing values
df = df.dropna()

# Convert pitch_type to dummy variables
df = pd.get_dummies(df, columns=[categorical_feature])

# ================================
# SPLIT DATA
# ================================
X = df.drop(columns=[target_x, target_z])
y_x = df[target_x]
y_z = df[target_z]

X_train, X_test, yx_train, yx_test = train_test_split(X, y_x, test_size=0.2, random_state=42)
_, _, yz_train, yz_test = train_test_split(X, y_z, test_size=0.2, random_state=42)
print("DATA LOADED AND CLEANED")
print(df.shape)
# ================================
# TRAIN MODELS
# ================================
model_x = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.05)
model_z = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.05)

model_x.fit(X_train, yx_train)
model_z.fit(X_train, yz_train)
print("TRAINING FINISHED")
# ================================
# EVALUATE MODEL
# ================================
pred_x = model_x.predict(X_test)
pred_z = model_z.predict(X_test)

mae_x = mean_absolute_error(yx_test, pred_x)
mae_z = mean_absolute_error(yz_test, pred_z)

rmse_x = np.sqrt(mean_squared_error(yx_test, pred_x))
rmse_z = np.sqrt(mean_squared_error(yz_test, pred_z))

print("\nModel Performance:")
print("Plate X MAE:", mae_x)
print("Plate Z MAE:", mae_z)
print("Plate X RMSE:", rmse_x)
print("Plate Z RMSE:", rmse_z)

# ================================
# SAVE MODELS
# ================================
joblib.dump(model_x, "model_plate_x.pkl")
joblib.dump(model_z, "model_plate_z.pkl")

print("\nModels saved")

# ================================
# SAVE SAMPLE PREDICTIONS (OPTIONAL)
# ================================
sample_df = X_test.copy()
sample_df["actual_x"] = yx_test.values
sample_df["actual_z"] = yz_test.values
sample_df["pred_x"] = pred_x
sample_df["pred_z"] = pred_z

sample_df["error_distance"] = np.sqrt(
    (sample_df["pred_x"] - sample_df["actual_x"])**2 +
    (sample_df["pred_z"] - sample_df["actual_z"])**2
)

sample_df.to_csv("676979_data_predictions.csv", index=False)

print("\nPredictions saved to 676979_data_predictions.csv")

# Show one example
print("\nSingle Pitch Example:")
print("Predicted:", pred_x[0], pred_z[0])
print("Actual:", yx_test.iloc[0], yz_test.iloc[0])
print("Error distance:", sample_df["error_distance"].iloc[0])