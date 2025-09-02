import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

DATA_DIR = '../data/processed'
MODELS_DIR = '../models'

data = pd.read_csv(f'{DATA_DIR}/metrics_data_no_outliers.csv')

# Feature & Target
X = data[['Days_Since_High_Last_7_Days', '%_Diff_From_High_Last_7_Days', 
    'Days_Since_Low_Last_7_Days', '%_Diff_From_Low_Last_7_Days']]

y_high = data['%_Diff_From_High_Next_5_Days']
y_low = data['%_Diff_From_Low_Next_5_Days']

# Split data into training and testing sets
X_train, X_test, y_high_train, y_high_test, y_low_train, y_low_test = train_test_split(
    X, y_high, y_low, test_size=0.2, random_state=42
)

models = {
    'LinearRegression': LinearRegression(),
    'RandomForest': RandomForestRegressor(random_state=42),
    'GradientBoosting': GradientBoostingRegressor(random_state=42),
    'SVR_poly': SVR(kernel='poly'),
    'SVR_rbf': SVR(kernel='rbf')
}

# Evaluating model performance
def evaluate_model(y_true, y_pred):
    mae = round(mean_absolute_error(y_true, y_pred), 4)
    mse = round(mean_squared_error(y_true, y_pred), 4)
    return {'MAE': mae, 'MSE': mse}

results_high = {}
for name, model in models.items():
    model.fit(X_train, y_high_train)
    y_pred = model.predict(X_test)
    results_high[name] = evaluate_model(y_high_test, y_pred)

results_low = {}
for name, model in models.items():
    model.fit(X_train, y_low_train)
    y_pred = model.predict(X_test)
    results_low[name] = evaluate_model(y_low_test, y_pred)

print("Evaluation Metrics for % Diff From High Next 5 Days Prediction:")
for name, metrics in results_high.items():
    print(f"{name}: {metrics}")

print("\nEvaluation Metrics for % Diff From Low Next 5 Days Prediction:")
for name, metrics in results_low.items():
    print(f"{name}: {metrics}")

# Select best model (lowest MAE) for each target
best_high = min(results_high, key=lambda k: results_high[k]['MAE'])
best_low = min(results_low, key=lambda k: results_low[k]['MAE'])

print(f"\nBest model for high prediction (lowest MAE): {best_high}")
print(f"Best model for low prediction (lowest MAE): {best_low}")

# Retrain best models on full data and save
os.makedirs(MODELS_DIR, exist_ok=True)
model_high = models[best_high]
model_low = models[best_low]
model_high.fit(X, y_high)
model_low.fit(X, y_low)
joblib.dump(model_high, f'{MODELS_DIR}/model_high.pkl')
joblib.dump(model_low, f'{MODELS_DIR}/model_low.pkl')
print("\nBest models saved as 'model_high.pkl' and 'model_low.pkl' in the models directory.")