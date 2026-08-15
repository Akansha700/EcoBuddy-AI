import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/electricity_energy_dataset.csv")

target = "MonthlyConsumptionKWh"

features = [
    "FamilyMembers",
    "FanHoursPerDay",
    "RefrigeratorHoursPerDay",
    "AirConditionerHoursPerDay",
    "TelevisionHoursPerDay",
    "MonitorHoursPerDay",
    "WashingMachineHoursPerWeek",
    "LightingHoursPerDay",
    "City",
    "Month",
    "TariffRateINRPerKWh"
]

X = df[features]
y = df[target]


# =========================
# PREPROCESSING
# =========================

numeric_features = [
    "FamilyMembers",
    "FanHoursPerDay",
    "RefrigeratorHoursPerDay",
    "AirConditionerHoursPerDay",
    "TelevisionHoursPerDay",
    "MonitorHoursPerDay",
    "WashingMachineHoursPerWeek",
    "LightingHoursPerDay",
    "Month",
    "TariffRateINRPerKWh"
]

categorical_features = ["City"]

preprocessor = ColumnTransformer([
    (
        "categorical",
        OneHotEncoder(handle_unknown="ignore"),
        categorical_features
    ),
    (
        "numeric",
        "passthrough",
        numeric_features
    )
])


# =========================
# TRAIN / TEST
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# =========================
# MODELS
# =========================

models = {
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}


# =========================
# TRAIN + COMPARE
# =========================

best_model = None
best_name = ""
best_r2 = float("-inf")

for name, algorithm in models.items():

    print(f"\nTraining {name}...")

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", algorithm)
    ])

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    mae = mean_absolute_error(y_test, prediction)
    rmse = mean_squared_error(y_test, prediction) ** 0.5
    r2 = r2_score(y_test, prediction)

    print(f"MAE  : {mae:.2f} kWh")
    print(f"RMSE : {rmse:.2f} kWh")
    print(f"R²   : {r2:.4f}")

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_name = name


# =========================
# SAVE BEST MODEL
# =========================

joblib.dump(
    {
        "model": best_model,
        "features": features
    },
    "models/energy_consumption_model.pkl"
)

print("\n" + "=" * 50)
print("BEST MODEL")
print("=" * 50)

print("Model:", best_name)
print(f"R²   : {best_r2:.4f}")

print("\nModel saved successfully!")
print("models/energy_consumption_model.pkl")