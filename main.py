import argparse
import logging

import folium
from matplotlib import pyplot as plt
from api_service import fetch_weather_data
from data_cleaning import clean_weather_data, detect_outliers
from report_generator import export_to_csv, export_to_excel, export_to_json, generate_pdf_report, generate_report, generate_comparison_report
from config import CITIES

logging.basicConfig(filename='app.log', level=logging.INFO)


def analyze_city(city, report_type, output_format):
    weather_data = fetch_weather_data(city)

    if weather_data:
        df = clean_weather_data(weather_data)

        if report_type in ['temperature', 'all']:
            df_clean_temp = detect_outliers(df, 'temperature', method='iqr')
            if output_format in ['pdf', 'all']:
                generate_pdf_report({city: df_clean_temp}, 'temperature')
            if output_format in ['csv', 'all']:
                export_to_csv({city: df_clean_temp})
            if output_format in ['excel', 'all']:
                export_to_excel({city: df_clean_temp})
            if output_format in ['json', 'all']:
                export_to_json({city: df_clean_temp})
        else:
            df_clean_temp = df  

        if report_type in ['humidity', 'all']:
            df_clean_humidity = detect_outliers(df_clean_temp, 'humidity', method='mad')
            if output_format in ['pdf', 'all']:
                generate_pdf_report({city: df_clean_humidity}, 'humidity')

    else:
        logging.error(f"Unable to fetch {city} weather report")


def analyze_cities(report_type, output_format='all', cities=None):
    df_dict = {}

    for city in cities:
        weather_data = fetch_weather_data(city)
        if weather_data:
            df = clean_weather_data(weather_data)
            if df is not None:
                if report_type in ['temperature', 'all']:
                    df_clean = detect_outliers(df, 'temperature', method='iqr')
                df_dict[city] = df_clean

    if output_format in ['pdf', 'all']:
        if report_type in ['temperature', 'all']:
            generate_pdf_report(df_dict, 'temperature', f'temperature_report_{"_".join(cities)}.pdf', cities)
        if report_type in ['humidity', 'all']:
            generate_pdf_report(df_dict, 'humidity', f'humidity_report_{"_".join(cities)}.pdf', cities)

    if output_format in ['csv', 'all']:
        export_to_csv(df_dict, cities)

    if output_format in ['excel', 'all']:
        export_to_excel(df_dict, cities)

    if output_format in ['json', 'all']:
        export_to_json(df_dict, cities)

    if output_format in ['map', 'all']:
        analyze_cities_with_map(cities)


def generate_report(df_dict, report_type):
    fig, ax = plt.subplots(figsize=(10, 6))

    for city, df in df_dict.items():
        if report_type == 'temperature':
            ax.plot(df['datetime'], df['temperature'], label=f'{city} Temperature')
        elif report_type == 'humidity':
            ax.plot(df['datetime'], df['humidity'], label=f'{city} Humidity')

    ax.set_title(f"Combined {report_type.capitalize()} Report for {', '.join(df_dict.keys())}")
    ax.set_xlabel('Datetime')
    ax.set_ylabel(f"{report_type.capitalize()} (°C)" if report_type == 'temperature' else f"{report_type.capitalize()} (%)")
    ax.legend()
    
    plt.show()

def analyze_cities_with_map(cities):
    city_data = []

    city_data = []

    for city in cities:
        weather_data = fetch_weather_data(city)
        if weather_data:
            df = clean_weather_data(weather_data)
            if df is not None:
                city_lat = weather_data['city']['coord']['lat']
                city_lon = weather_data['city']['coord']['lon']
                temperature = df['temperature'].mean()  
                humidity = df['humidity'].mean()  

                city_data.append({
                    "city": city,
                    "lat": city_lat,
                    "lon": city_lon,
                    "temperature": temperature,
                    "humidity": humidity
                })

    map_center = [city_data[0]['lat'], city_data[0]['lon']]  # 以第一个城市为中心
    weather_map = folium.Map(location=map_center, zoom_start=3)

    for city_info in city_data:
        city_name = city_info['city']
        lat = city_info['lat']
        lon = city_info['lon']
        popup_info = f"{city_name}: Temperature: {city_info['temperature']}°C, Humidity: {city_info['humidity']}%"
        folium.Marker([lat, lon], popup=popup_info).add_to(weather_map)


    map_filename = f"weather_map_{'_'.join(cities)}.html"
    weather_map.save(map_filename)
    print(f"Map Saved as : {map_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Data Analysis Tool")

    parser.add_argument(
        '--city',
        nargs='+',
        help='Specify the city to generate weather data, if not provided would generate a set of cities',
        default=None
    )

    parser.add_argument(
        '--report',
        type=str,
        choices=['temperature', 'humidity', 'all'],
        help='Specify the report type: temperature, humidity or all',
        default='all'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['pdf', 'csv', 'excel', 'json', 'map', 'all'],
        help='Specify the output file format: pdf, csv, excel, json, map or all.',
        default='all'
    )


    args = parser.parse_args()

    if args.city:
        analyze_cities(args.report, args.format, args.city)
