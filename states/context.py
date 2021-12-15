from __future__ import annotations

import logging

import telebot.types

from UserProperties import UserProperties


class Bot:
    _state = None

    def __init__(self, message: telebot.types.Message, intent: str):
        user_id = message.from_user.id
        self.properties, _ = UserProperties.get_or_create(id=user_id)
        logging.debug(self.properties)
        if self.properties.state == 'start':
            self.set_state(StartState(message, intent))
        elif self.properties.state == 'setLocation':
            self.set_state(SetLocationState(message, intent))

    def set_state(self, state: AbstractState):
        self._state = state
        self._state.context = self
        self.properties = UserProperties.get_by_id(self.properties.id)
        self.properties.state = state.name
        self.properties.save()

    def run(self) -> str:
        return self._state.run()


from .AbstractState import AbstractState
from .StartState import StartState
from .SetLocationState import SetLocationState
