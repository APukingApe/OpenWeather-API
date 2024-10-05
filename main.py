from api_service import fetch_weather_data
from data_cleaning import clean_weather_data, detect_outliers_iqr
from report_generator import generate_report
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    
    if weather_data:
        df = clean_weather_data(weather_data)
        
        if df is not None:
            df_clean_temp = detect_outliers_iqr(df, 'temperature')
            df_clean_humidity = detect_outliers_iqr(df_clean_temp, 'humidity')
            
            generate_report(df, df_clean_humidity)
        else:
            logging.error("Data washing error")
    else:
        logging.error("Unable to generate report")
