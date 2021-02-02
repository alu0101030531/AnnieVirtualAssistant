import geocoder
import requests
import pyowm


class WeatherRequest:
    def __init__(self):
        self.weatherKey = 'de2411c4d0cdca5f3f257bc5bf135675'
        self.OpenWMap = pyowm.OWM(self.weatherKey).weather_manager()


    def getWeather(self, city):
        weather_info = ""
        obs = self.OpenWMap.weather_at_place(city)
        data = obs.weather
        temp = data.temperature(unit='celsius')
        weather_info += "In " + city + " the average temperature is " + str(temp['temp']) + " the maximum temperature is " + str(temp['temp_max']) + \
                        "and minimum temperature is " + str(temp['temp_min'])

        return weather_info
