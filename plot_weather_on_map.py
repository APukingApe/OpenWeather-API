import folium

def plot_weather_on_map(city_data, map_filename='weather_map.html'):
    # Create map and set center
    map_center = [city_data[0]['lat'], city_data[0]['lon']]  
    weather_map = folium.Map(location=map_center, zoom_start=3)

    for city_info in city_data:
        city_name = city_info['city']
        lat = city_info['lat']
        lon = city_info['lon']
        temperature = city_info['temperature']
        humidity = city_info['humidity']

        marker_color = get_color_by_temperature(temperature)

        popup_info = f"{city_name}:<br>Temperature: {temperature}°C<br>Humidity: {humidity}%"
        folium.Marker(
            location=[lat, lon],
            popup=popup_info,
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(weather_map)

    weather_map.save(map_filename)
    print(f"Map Saved as {map_filename}")

def get_color_by_temperature(temperature):
    if temperature < 10:
        return 'blue'
    elif 10 <= temperature < 20:
        return 'green'
    else:
        return 'red'