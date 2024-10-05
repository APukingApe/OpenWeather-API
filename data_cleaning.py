import pandas as pd
import numpy as np
import logging

def clean_weather_data(data):
    """Clean weather data and transform them into DataFrame"""
    weather_list = data['list']
    df = pd.DataFrame([{
        "datetime": item["dt_txt"],
        "temperature": item["main"]["temp"],
        "humidity": item["main"]["humidity"]
    } for item in weather_list])
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    return df


def detect_outliers_iqr(df, column):
    """Use IQR to detect Outlier"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df_clean = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df_clean
