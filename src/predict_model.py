import pandas as pd
import joblib

MODELS_DIR = '../models'

def predict_outcomes(days_since_high, diff_from_high, days_since_low, diff_from_low):
    model_high = joblib.load(f'{MODELS_DIR}/model_high.pkl')
    model_low = joblib.load(f'{MODELS_DIR}/model_low.pkl')
    
    # Prepare the input DataFrame for prediction
    X_new = pd.DataFrame([[days_since_high, diff_from_high, days_since_low, diff_from_low]], 
                        columns=['Days_Since_High_Last_7_Days', '%_Diff_From_High_Last_7_Days', 
                                'Days_Since_Low_Last_7_Days', '%_Diff_From_Low_Last_7_Days'])
    
    # Predict outcomes and round to 2 decimal places
    high_pred = round(float(model_high.predict(X_new)[0]), 2)
    low_pred = round(float(model_low.predict(X_new)[0]), 2)
    
    return {
        'Predicted % Diff From High Next 5 Days': high_pred,
        'Predicted % Diff From Low Next 5 Days': low_pred
    }

# Sample Prediction
if __name__ == "__main__":
    example_prediction = predict_outcomes(3, -1.5, 4, -2.0)
    print("\nExample Prediction for New Input Data:")
    print(example_prediction)