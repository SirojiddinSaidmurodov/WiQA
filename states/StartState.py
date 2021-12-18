import os

import dotenv
from pyowm.owm import OWM

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
        return 'start'

    def action_exit(self):
        return "Bot state has been reset already"

    def action_weather(self):
        properties: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
        if properties.lat is None:
            self.context.set_state(SetLocationState(self.message, self.intent))
            return "Please, send your location in order to get weather forecast"
        else:
            w = manager.weather_at_coords(lat=properties.lat, lon=properties.long)
            output = {"clouds": w.weather.clouds, "rain": w.weather.rain, "snow": w.weather.snow, "wind": w.weather.wnd,
                      "humidity": w.weather.humidity, "pressure": w.weather.pressure,
                      "temperature": w.weather.temperature("celsius"), "status": w.weather.detailed_status,
                      "sunrise": w.weather.sunrise_time('date'), "sunset": w.weather.sunset_time('date')}
            return str(output)


from UserProperties import UserProperties
from states.SetLocationState import SetLocationState
from states.QueryState import QueryState
