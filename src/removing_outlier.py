import pandas as pd

DATA_PATH = '../data/processed/metrics_data.csv'
OUTPUT_PATH = '../data/processed/metrics_data_no_outliers.csv'

metrics_data = pd.read_csv(DATA_PATH)

def drop_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[col] >= lower) & (df[col] <= upper)]

metrics_data = drop_outliers(metrics_data, 'High')
metrics_data = drop_outliers(metrics_data, 'Low')

metrics_data.to_csv(OUTPUT_PATH, index=False)
print(f"Saved cleaned data to {OUTPUT_PATH}")