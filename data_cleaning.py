import pandas as pd
import numpy as np
import logging

from scipy import stats

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

def detect_outliers_zscore(df, column, threshold=3):
    """Use Z-score algorithm"""
    z_scores = stats.zscore(df[column])
    abs_z_scores = np.abs(z_scores)
    df_clean = df[abs_z_scores < threshold]
    
    return df_clean

def detect_outliers_mad(df, column, threshold=3):
    """Use mad algorithm"""
    median = np.median(df[column])
    mad = np.median(np.abs(df[column] - median))
    modified_z_scores = 0.6745 * (df[column] - median) / mad
    
    df_clean = df[np.abs(modified_z_scores) < threshold]
    
    return df_clean

def detect_outliers(df, column, method="iqr", threshold=3):

    if method == "iqr":
        return detect_outliers_iqr(df, column)
    elif method == "zscore":
        return detect_outliers_zscore(df, column, threshold)
    elif method == "mad":
        return detect_outliers_mad(df, column, threshold)
    else:
        logging.error(f"Undefined method: {method}")
        return df  