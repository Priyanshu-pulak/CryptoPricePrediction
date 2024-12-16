# Cryptocurrency Price Prediction

## Overview
This project aims to predict the percentage difference in cryptocurrency prices using historical data. By analyzing past high and low prices, the model can forecast potential future price movements.

## Installation
To install the required packages, run:
pip install -r requirements.txt

## Project Steps

### 1. Data Retrieval
The first step involves fetching historical cryptocurrency price data using the CoinGecko API. This data includes daily open, high, low, and close prices for a specified cryptocurrency over the last 90 days.

### 2. Metric Calculation
Once the data is retrieved, various metrics are calculated to assist in predictions. These metrics include:
- Historical High and Low Prices for the past specified days (e.g., 7 days).
- Days Since High and Low Prices for the past specified days.
- Percentage differences from the historical highs and lows.
- Future High and Low Prices for a specified number of days ahead (e.g., 5 days).
- Percentage differences from the future high and low prices.

The processed data is saved to an Excel file for further use.

### 3. Machine Learning Model
A machine learning model, specifically a Linear Regression model, is trained using the calculated metrics. The features (input variables) include:
- Days Since High and Low for the last 7 days.
- Percentage differences from the historical highs and lows.

The target variables (output variables) are the percentage differences from the future high and low prices for the next 5 days. The dataset is split into training and testing sets to evaluate the model's performance.

### 4. Evaluation and Predictions
After training the models, their performance is evaluated using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), and R-squared (R²). The trained models are saved for future predictions.

A function is provided to make predictions based on new input data, allowing users to estimate future price movements based on the calculated metrics.

## Usage
1. Retrieve historical data by invoking the data retrieval function.
2. Calculate necessary metrics from the retrieved data.
3. Train the machine learning model with the calculated metrics.
4. Use the prediction function to forecast future price differences based on new input values.

## License
This project is licensed under the MIT License.

## Acknowledgments
CoinGecko API for providing historical price data.

## Conclusion
This project demonstrates how historical price data can be leveraged to predict future cryptocurrency prices using machine learning techniques. The results can help investors make informed decisions in the volatile cryptocurrency market.