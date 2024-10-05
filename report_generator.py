import matplotlib.pyplot as plt
import seaborn as sns

def generate_report(df, df_clean):
    """Generates a report of temperature and humidity"""
    
    sns.set(style="whitegrid")

    # Visualize raw data
    plt.figure(figsize=(10, 6))
    plt.plot(df['datetime'], df['temperature'], label='Original Temperature', color='blue')
    plt.plot(df_clean['datetime'], df_clean['temperature'], label='Cleaned Temperature', color='green')
    plt.title("Temperature Over Time (with and without outliers)")
    plt.xlabel("Datetime")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.savefig('temperature_report.png')
    plt.show()

    # Washed data
    plt.figure(figsize=(10, 6))
    plt.plot(df_clean['datetime'], df_clean['humidity'], label='Cleaned Humidity', color='purple')
    plt.title("Cleaned Humidity Over Time")
    plt.xlabel("Datetime")
    plt.ylabel("Humidity (%)")
    plt.legend()
    plt.savefig('humidity_report.png')
    plt.show()
    

