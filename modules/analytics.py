import pandas as pd

def category_summary(df):
    return df.groupby("category")["amount"].sum()

def monthly_summary(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    return df.groupby('month')['amount'].sum()