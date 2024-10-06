from api_service import fetch_weather_data
from data_cleaning import clean_weather_data, detect_outliers
from report_generator import generate_comparison_report, generate_report
from config import CITIES
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)

if __name__ == "__main__":
    df_dict = {}

    for city in CITIES:
        weather_data = fetch_weather_data(city)
        
        if weather_data:
            df = clean_weather_data(weather_data)
            
            if df is not None:
                df_clean_temp = detect_outliers(df, 'temperature', method='iqr')
                df_clean_humidity = detect_outliers(df_clean_temp, 'humidity', method='mad')
                
                df_dict[city] = df_clean_humidity
                
                generate_report(df, df_clean_humidity, 'temperature', city)
                generate_report(df, df_clean_humidity, 'humidity', city)
            else:
                logging.error(f"{city} 的数据清洗失败")
        else:
            logging.error(f"未能获取 {city} 的天气数据")
    
    # 生成多个城市的对比报告
    generate_comparison_report(df_dict, 'temperature')
    generate_comparison_report(df_dict, 'humidity')
