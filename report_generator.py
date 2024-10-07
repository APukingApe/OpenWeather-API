import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

def generate_report(df, df_clean, column, city):
    """Generates a report of temperature and humidity"""
    
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plt.plot(df['datetime'], df[column], label=f'Original {column.capitalize()}', color='blue', alpha=0.5)
    plt.plot(df_clean['datetime'], df_clean[column], label=f'Cleaned {column.capitalize()}', color='green')
    plt.title(f"{city} {column.capitalize()} Over Time (with and without outliers)")
    plt.xlabel("Datetime")
    plt.ylabel(f"{column.capitalize()} ({'°C' if column == 'temperature' else '%'})")
    plt.legend()
    
    filename = f'{city}_{column}_report.png'
    plt.savefig(filename)
    plt.show()

def generate_combined_pdf_report(df_dict, report_type, filename, cities):
    with PdfPages(filename) as pdf:
        fig, ax = plt.subplots(figsize=(10, 6))

        for city, df in df_dict.items():
            if report_type == 'temperature' and 'temperature' in df.columns:
                ax.plot(df['datetime'], df['temperature'], label=f'{city} Temperature')
            elif report_type == 'humidity' and 'humidity' in df.columns:
                ax.plot(df['datetime'], df['humidity'], label=f'{city} Humidity')

        ax.set_title(f"Combined {report_type.capitalize()} Report for {', '.join(cities)}")
        ax.set_xlabel('Datetime')
        ax.set_ylabel(f"{report_type.capitalize()} (°C)" if report_type == 'temperature' else f"{report_type.capitalize()} (%)")
        ax.legend()

        pdf.savefig(fig)
        plt.close()

    print(f"{report_type} PDF report Generated：{filename}")

def export_combined_to_csv(df_dict, cities):
    filename = f"weather_data_{'_'.join(cities)}.csv"
    combined_df = pd.DataFrame()

    for city, df in df_dict.items():
        df_copy = df.copy()
        df_copy['city'] = city  # 在每个数据行中添加城市名称
        combined_df = pd.concat([combined_df, df_copy])

    combined_df.to_csv(filename, index=False)
    print(f"Mered CSV exported to：{filename}")

def export_combined_to_excel(df_dict, cities):
    filename = f"weather_data_{'_'.join(cities)}.xlsx"

    combined_df = pd.DataFrame()

    for city, df in df_dict.items():
        df_copy = df.copy()
        df_copy['city'] = city  
        combined_df = pd.concat([combined_df, df_copy])

    with pd.ExcelWriter(filename) as writer:
        combined_df.to_excel(writer, index=False)

    print(f"Mered Excel exported to：{filename}")

def export_combined_to_json(df_dict, cities):
    filename = f"weather_data_{'_'.join(cities)}.json"

    combined_df = pd.DataFrame()

    for city, df in df_dict.items():
        df_copy = df.copy()
        df_copy['city'] = city  
        combined_df = pd.concat([combined_df, df_copy])

    combined_df.to_json(filename, orient='records', lines=True)

    print(f"Mered JSON exported to：{filename}")   

def generate_comparison_report(df_dict, column):
    """Generates a comparison report"""
    
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    for city, df in df_dict.items():
        plt.plot(df['datetime'], df[column], label=city)
    
    plt.title(f"Comparison of {column.capitalize()} Across Cities")
    plt.xlabel("Datetime")
    plt.ylabel(f"{column.capitalize()} ({'°C' if column == 'temperature' else '%'})")
    plt.legend()
    filename = f'comparison_{column}_report.png'
    plt.savefig(filename)
    plt.show()

def generate_pdf_report(df, df_clean, city):
    with PdfPages(f'{city}_weather_report.pdf') as pdf:
        plt.figure()
        plt.plot(df['datetime'], df['temperature'], label='Original Temperature', color='blue')
        plt.plot(df_clean['datetime'], df_clean['temperature'], label='Cleaned Temperature', color='green')
        plt.title(f"{city} Temperature Over Time")
        plt.xlabel('Datetime')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure()
        plt.plot(df['datetime'], df['humidity'], label='Original Humidity', color='red')
        plt.plot(df_clean['datetime'], df_clean['humidity'], label='Cleaned Humidity', color='purple')
        plt.title(f"{city} Humidity Over Time")
        plt.xlabel('Datetime')
        plt.ylabel('Humidity (%)')
        plt.legend()
        pdf.savefig() 
        plt.close()

    print(f"{city} report is generate: {city}_weather_report.pdf")

def export_to_json(df_clean, city):
    json_file = f"{city}_cleaned_weather_data.json"
    df_clean.to_json(json_file, orient='records', lines=True)
    print(f"Washed data exported to JSON: {json_file}")

def export_to_excel(df_clean, city):
    excel_file = f"{city}_cleaned_weather_data.xlsx"
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df_clean.to_excel(writer, sheet_name='Cleaned Data', index=False)
    print(f"Washed data exported to Excel: {excel_file}")

def export_to_csv(df_clean, city):
    csv_file = f"{city}_cleaned_weather_data.csv"
    df_clean.to_csv(csv_file, index=False)
    print(f"Washed data exported to CSV: {csv_file}")