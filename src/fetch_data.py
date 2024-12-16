import requests
import pandas as pd 
from datetime import datetime  

def fetch_crypto_data(crypto_pair, start_date):
        
    vs_currency = 'usd'
    api_url = f'https://api.coingecko.com/api/v3/coins/{crypto_pair}/market_chart?vs_currency={vs_currency}&days=90'
    # Constructing the API URL to fetch market data for the last 90 days

    # Make a GET request to the API
    response = requests.get(api_url)  
    if response.status_code != 200:
        
        # Check if the request was successful (status code 200)
        raise Exception(f"Failed to fetch data: {response.status_code}")

    # Parse the JSON response
    data = response.json()  
    records = []

    for entry in data['prices']:
        # Loop through each entry in the 'prices' data
        timestamp, close_price = entry
        record = {
            'Date': datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d'),
            'Open': close_price * 0.99, 
            'High': close_price * 1.01, 
            'Low': close_price * 0.98,
            'Close': close_price
        }
        records.append(record)

    # Create a DataFrame from the records list
    df = pd.DataFrame(records)

    # Filter the DataFrame to include only records from the specified start date
    df = df[df['Date'] >= start_date]

    # Save the DataFrame to an Excel file in the specified path
    df.to_excel("../data/processed/crypto_data.xlsx", index=False)
    return df 

# Try-except block to handle potential exceptions when fetching data
try:
    # Call the function to fetch cryptocurrency data for Bitcoin starting from January 1, 2024
    crypto_data = fetch_crypto_data("bitcoin", "2024-01-01")
    print(crypto_data.head())
except Exception as e:
    print(e)