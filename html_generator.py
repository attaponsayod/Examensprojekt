def generate_html(weather_data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Data</title>
    </head>
    <body>
        <h1>Weather Information for {weather_data['city']}</h1>
        <table border="1">
            <tr>
                <th>City</th>
                <th>Temperature (C)</th>
                <th>Humidity (%)</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>{weather_data['city']}</td>
                <td>{weather_data['temperature']}</td>
                <td>{weather_data['humidity']}</td>
                <td>{weather_data['description']}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    # Save the content to an HTML file
    with open("webb_app.html", "w") as file:
        file.write(html_content)
    print("Program is running")

# Example usage
if __name__ == "__main__":
    sample_weather_data = {
        "city": "Stockholm",
        "temperature": 10.5,
        "humidity": 80,
        "description": "clear sky"
    }
    generate_html(sample_weather_data)
