import pandas as pd
import numpy as np

def clean_data(df):
   
    def fill_missing_values(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

        object_cols = df.select_dtypes(include=[object]).columns
        df[object_cols] = df[object_cols].fillna(df[object_cols].mode().iloc[0])
        return df

    def handle_outliers(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[col] = np.where((df[col] < lower_bound) | (df[col] > upper_bound), np.nan, df[col])
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        return df

    def convert_data_types(df):
        df['Start'] = pd.to_datetime(df['Start'], errors='coerce')
        df['End'] = pd.to_datetime(df['End'], errors='coerce')
        categorical_cols = ['Handset Manufacturer', 'Handset Type', 'Last Location Name']
        for col in categorical_cols:
            df[col] = df[col].astype('category')
        return df

    df = fill_missing_values(df)
    df = handle_outliers(df)
    df = convert_data_types(df)
    
    return df