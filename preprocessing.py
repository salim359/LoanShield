import pandas as pd

def preprocess_input(df, X_columns):
    df = df.drop(columns=['Gender','ID'], errors='ignore')
    df = df.fillna(df.median(numeric_only=True))
    df = pd.get_dummies(df, drop_first=True)
    df = df.reindex(columns=X_columns, fill_value=0)
    return df