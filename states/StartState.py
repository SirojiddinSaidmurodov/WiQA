import os

import dotenv
from pyowm.owm import OWM
from pyowm.weatherapi25.location import Location
from pyowm.weatherapi25.observation import Observation
from pyowm.weatherapi25.weather import Weather

from states.AbstractState import AbstractState

dotenv.load_dotenv()
owm = OWM(os.environ.get("owm_token"))
manager = owm.weather_manager()


class StartState(AbstractState):

    def action_set_context(self):
        self.context.set_state(QueryState(self.message, self.intent))
        return "Give me a subject to search"

    @property
    def name(self):
        return "start"

    def action_exit(self):
        return "Bot state has been reset already"

    def action_weather(self):
        properties: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
        if properties.lat is None:
            self.context.set_state(SetLocationState(self.message, self.intent))
            return "Please, send your location in order to get weather forecast"
        else:
            w: Observation = manager.weather_at_coords(lat=properties.lat, lon=properties.long)
            latlon_res: Location = w.location
            city = latlon_res.name
            lat = properties.lat
            lon = properties.long
            weather: Weather = w.weather
            wind_res = weather.wnd
            wind_speed = str(wind_res.get('speed'))

            humidity = str(weather.humidity.real)

            celsius_result = weather.temperature('celsius')
            temp_min_celsius = str(celsius_result.get('temp_min'))
            temp_max_celsius = str(celsius_result.get('temp_max'))
            output = "Today the weather in " + str(city) \
                     + ": \n" + "🌡Temperature:\n        Max temp :" + str(temp_max_celsius) \
                     + "℃\n        Min Temp :" + str(temp_min_celsius) + "℃\n💧Humidity :" + str(humidity) \
                     + "%\n💨Wind Speed :" + str(wind_speed) \
                     + "\nLocation:\n       Latitude :" + str(lat) + "\n       Longitude :" + str(lon)
            return str(output)


from UserProperties import UserProperties
from states.SetLocationState import SetLocationState
from states.QueryState import QueryState
