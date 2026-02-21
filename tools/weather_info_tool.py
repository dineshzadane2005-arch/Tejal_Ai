import os
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        # Only setup tools if API key is available
        if self.api_key and self.api_key != "your-openweathermap-key-here":
            try:
                from utils.weather_info import WeatherForecastTool
                self.weather_service = WeatherForecastTool(self.api_key)
                self.weather_tool_list = self._setup_tools()
            except Exception as e:
                print(f"Weather tools disabled: {e}")
                self.weather_tool_list = []
        else:
            print("Weather API key not found. Weather features disabled.")
            self.weather_tool_list = []
    
    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Weather information not available for {city}"
        
        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            forecast_data = self.weather_service.get_forecast_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celsius, {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Weather forecast not available for {city}"
    
        return [get_current_weather, get_weather_forecast]