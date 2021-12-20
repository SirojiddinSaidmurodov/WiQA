import logging

from states.AbstractState import AbstractState


class SetLocationState(AbstractState):
    @property
    def name(self) -> str:
        return 'setLocation'

    def run(self):
        if self.message.content_type != "location":
            super().run()
        else:
            properties: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
            logging.debug(self.message.location)

            properties.lat = self.message.location.latitude
            properties.long = self.message.location.longitude
            properties.save()
            self.context.set_state(StartState(self.message, self.intent))
            return "Location is set"

    def action_weather(self):
        return "Please, send me your location in order to get weather forecast"

    def action_set_context(self):
        return "Send your location first"

    def action_info(self):
        return "Send your location first"

    def action_greeting(self):
        return "Send your location first"

    def action_exit(self):
        self.context.set_state(StartState(self.message, self.intent))
        return "State is reset"


from states.StartState import StartState
from UserProperties import UserProperties
