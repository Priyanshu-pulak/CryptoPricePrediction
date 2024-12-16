import pandas as pd

def calculate_metrics(data, variable1, variable2):
    
    # Ensure the Date column is a datetime object
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Calculate Historical High and Low Prices for the past `variable1` days
    data[f'High_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).max()
    data[f'Low_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).min()

    # Calculate Days Since High and Low for the past `variable1` days
    data[f'Days_Since_High_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).apply(lambda x: (x.argmax() + 1), raw=True)
    data[f'Days_Since_Low_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).apply(lambda x: (x.argmin() + 1), raw=True)

    # Calculate % Difference from Historical High and Low Prices
    data[f'%_Diff_From_High_Last_{variable1}_Days'] = ((data['Close'] - data[f'High_Last_{variable1}_Days']) / data[f'High_Last_{variable1}_Days']) * 100
    data[f'%_Diff_From_Low_Last_{variable1}_Days'] = ((data['Close'] - data[f'Low_Last_{variable1}_Days']) / data[f'Low_Last_{variable1}_Days']) * 100

    # Calculate Future High and Low Prices for the next `variable2` days
    data[f'High_Next_{variable2}_Days'] = data['Close'].shift(-variable2).rolling(window=variable2).max()
    data[f'Low_Next_{variable2}_Days'] = data['Close'].shift(-variable2).rolling(window=variable2).min()

    # Calculate % Difference from Future High and Low Prices
    data[f'%_Diff_From_High_Next_{variable2}_Days'] = ((data['Close'] - data[f'High_Next_{variable2}_Days']) / data[f'High_Next_{variable2}_Days']) * 100
    data[f'%_Diff_From_Low_Next_{variable2}_Days'] = ((data['Close'] - data[f'Low_Next_{variable2}_Days']) / data[f'Low_Next_{variable2}_Days']) * 100

    # Drop rows with NaN values resulting from rolling calculations
    data.dropna(inplace=True)

    # Save the calculated metrics to an Excel file
    data.to_excel("../data/processed/metrics_data.xlsx", index=False)
    return data

# Load the historical data from crypto_data.xlsx
data = pd.read_excel("../data/processed/crypto_data.xlsx")

# Define variables for the look-back and look-forward periods
variable1 = 7
variable2 = 5 

# Calculate the metrics
metrics_data = calculate_metrics(data, variable1, variable2)

# Display the first few rows of the calculated data for verification
print(metrics_data.head())
