import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Load and preprocess data
data = pd.read_excel('../data/processed/metrics_data.xlsx')

# Define features (input variables) and targets (output variables)
X = data[['Days_Since_High_Last_7_Days', '%_Diff_From_High_Last_7_Days', 
    'Days_Since_Low_Last_7_Days', '%_Diff_From_Low_Last_7_Days']]

y_high = data['%_Diff_From_High_Next_5_Days']
y_low = data['%_Diff_From_Low_Next_5_Days']

# Split data into training and testing sets
X_train, X_test, y_high_train, y_high_test, y_low_train, y_low_test = train_test_split(
    X, y_high, y_low, test_size=0.2, random_state=42
)

# Initialize the Linear Regression models
model_high = LinearRegression()
model_low = LinearRegression()

# Train the models
model_high.fit(X_train, y_high_train)
model_low.fit(X_train, y_low_train)

# Make predictions on the test set
y_high_pred = model_high.predict(X_test)
y_low_pred = model_low.predict(X_test)

# Evaluate model performance
def evaluate_model(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {'MAE': mae, 'MSE': mse, 'R2': r2}

# Print evaluation metrics for both models
print("Evaluation Metrics for % Diff From High Next 5 Days Prediction:")
print(evaluate_model(y_high_test, y_high_pred))

print("\nEvaluation Metrics for % Diff From Low Next 5 Days Prediction:")
print(evaluate_model(y_low_test, y_low_pred))

# Create the models directory if it doesn't exist
os.makedirs('../models', exist_ok=True)

# Save the trained models to the models directory
joblib.dump(model_high, '../models/model_high.pkl')
joblib.dump(model_low, '../models/model_low.pkl')
print("\nModels saved as 'model_high.pkl' and 'model_low.pkl' in the models directory.")