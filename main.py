import argparse
import logging
from api_service import fetch_weather_data
from data_cleaning import clean_weather_data, detect_outliers
from report_generator import generate_report, generate_comparison_report
from config import CITIES

# 配置日志
logging.basicConfig(filename='app.log', level=logging.INFO)


def analyze_city(city, report_type):
    weather_data = fetch_weather_data(city)

    if weather_data:
        df = clean_weather_data(weather_data)

        if report_type in ['temperature', 'all']:
            df_clean_temp = detect_outliers(df, 'temperature', method='iqr')
            generate_report(df, df_clean_temp, 'temperature', city)
        else:
            df_clean_temp = df  

        if report_type in ['humidity', 'all']:
            df_clean_humidity = detect_outliers(df_clean_temp, 'humidity', method='mad')
            generate_report(df, df_clean_humidity, 'humidity', city)

    else:
        logging.error(f"未能获取 {city} 的天气数据")


def analyze_multiple_cities(report_type):
    df_dict = {}

    for city in CITIES:
        weather_data = fetch_weather_data(city)

        if weather_data:
            df = clean_weather_data(weather_data)

            if df is not None:
                df_clean = df

                if report_type in ['temperature', 'all']:
                    df_clean = detect_outliers(df_clean, 'temperature', method='iqr')
                if report_type in ['humidity', 'all']:
                    df_clean = detect_outliers(df_clean, 'humidity', method='mad')

                df_dict[city] = df_clean

                if report_type in ['temperature', 'all']:
                    generate_report(df, df_clean, 'temperature', city)
                if report_type in ['humidity', 'all']:
                    generate_report(df, df_clean, 'humidity', city)

        else:
            logging.error(f"Unalbe to get {city}")

    if report_type in ['temperature', 'all']:
        generate_comparison_report(df_dict, 'temperature')
    if report_type in ['humidity', 'all']:
        generate_comparison_report(df_dict, 'humidity')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Data Analysis Tool")

    parser.add_argument(
        '--city',
        type=str,
        help='Point the city to generate weather data, if not provided would generate a set of cities',
        default=None
    )

    parser.add_argument(
        '--report',
        type=str,
        choices=['temperature', 'humidity', 'all'],
        help='Point the report type, temperature, humidity or all',
        default='all'
    )

    args = parser.parse_args()

    if args.city:
        analyze_city(args.city, args.report)
    else:
        analyze_multiple_cities(args.report)
