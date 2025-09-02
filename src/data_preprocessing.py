import pandas as pd

DATA_DIR = '../data/processed'

data = pd.read_excel(f'{DATA_DIR}/crypto_data.xlsx')

def calculate_metrics(data, variable1, variable2):

    # Ensure the Date column is a datetime object
    data['Date'] = pd.to_datetime(data['Date'])

    # Historical High and Low Prices for the past 'variable1' minutes
    data[f'High_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).max()
    data[f'Low_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).min()

    # Days Since High and Low for the past 'variable1' minutes
    data[f'Days_Since_High_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).apply(lambda x: (x.argmax() + 1), raw=True)
    data[f'Days_Since_Low_Last_{variable1}_Days'] = data['Close'].rolling(window=variable1).apply(lambda x: (x.argmin() + 1), raw=True)

    # % Difference from Historical High and Low Prices
    data[f'%_Diff_From_High_Last_{variable1}_Days'] = ((data['Close'] - data[f'High_Last_{variable1}_Days']) / data[f'High_Last_{variable1}_Days']) * 100
    data[f'%_Diff_From_Low_Last_{variable1}_Days'] = ((data['Close'] - data[f'Low_Last_{variable1}_Days']) / data[f'Low_Last_{variable1}_Days']) * 100
    
    # Future High and Low Prices for the next 'variable2' minutes
    data[f'High_Next_{variable2}_Days'] = data['Close'].shift(-variable2).rolling(window=variable2).max()
    data[f'Low_Next_{variable2}_Days'] = data['Close'].shift(-variable2).rolling(window=variable2).min()

    # % Difference from Future High and Low Prices
    data[f'%_Diff_From_High_Next_{variable2}_Days'] = ((data['Close'] - data[f'High_Next_{variable2}_Days']) / data[f'High_Next_{variable2}_Days']) * 100
    data[f'%_Diff_From_Low_Next_{variable2}_Days'] = ((data['Close'] - data[f'Low_Next_{variable2}_Days']) / data[f'Low_Next_{variable2}_Days']) * 100
    
    # Drop rows with NaN values resulting from rolling calculations
    data.dropna(inplace=True)

    for col in data.columns:
        if '%' in col:
            data[col] = data[col].round(4)
        elif 'Days_Since' in col:
            data[col] = data[col].astype(int)
        elif col != 'Date':
            data[col] = data[col].round(2)

    data.to_csv(f'{DATA_DIR}/metrics_data.csv', index=False)
    return data

variable1 = 7
variable2 = 5 

metrics_data = calculate_metrics(data, variable1, variable2)

print(metrics_data.head())
