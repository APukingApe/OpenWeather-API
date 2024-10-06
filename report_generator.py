import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # 保存为以城市命名的报告文件
    filename = f'{city}_{column}_report.png'
    plt.savefig(filename)
    plt.show()

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

