from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import telebot.types

import states
from UserProperties import UserProperties


class BotContext:
    _state = None

    def __init__(self, message: telebot.types.Message):
        user_id = message.from_user.id
        self.properties, _ = UserProperties.get_or_create(id=user_id)
        logging.debug(self.properties)
        if self.properties.state == 'start':
            self.set_state(StartState(message))

    def set_state(self, state: State):
        self._state = state
        self._state.context = self
        self.properties.state = state.name
        self.properties.save()

    def run(self) -> str:
        return self._state.run()


class State(ABC):

    def __init__(self, message: telebot.types.Message):
        self.message = message
        self._context = None

    @property
    def context(self) -> BotContext:
        return self._context

    @context.setter
    def context(self, context: BotContext) -> None:
        self._context = context

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self):
        pass

    def greeting(self):
        pass

    def weather(self):
        pass

    def info(self):
        pass

    def set_text_context(self):
        pass

    @abstractmethod
    def exit(self):
        pass


class StartState(State):

    def exit(self):
        self.context.set_state(StartState(message=self.message))
        return "Состояние бота сброшено!"

    def run(self):
        text: str = self.message.text
        logging.debug(text)
        logging.debug(states.intent_catcher_model([text]))

        intent = states.intent_catcher_model([text])[0]
        if intent == 'greeting':
            return self.greeting()
        if intent == 'weather_forecast_intent':
            return self.weather()
        if intent == 'info':
            return self.info()
        if intent == 'exit':
            return self.exit()
        if intent == 'context':
            return self.set_text_context()

    @property
    def name(self):
        return 'start'

    def greeting(self):
        return "Привет!"

    def weather(self):
        properties: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
        if properties.lat is None:
            self.context.set_state(GetLocationState(message=self.message))
            return "Отправьте свою геопозицию"


class GetLocationState(State):

    def exit(self):
        self.context.set_state(StartState(message=self.message))
        return "Состояние бота сброшено!"

    @property
    def name(self) -> str:
        return 'location'

    def run(self):
        pass
