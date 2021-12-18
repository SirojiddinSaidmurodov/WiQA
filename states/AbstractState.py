from abc import ABC, abstractmethod

import telebot.types

from states.context import Bot


class AbstractState(ABC):

    def __init__(self, message: telebot.types.Message, intent: str):
        self.message = message
        self.intent = intent
        self._context = None

    @property
    def context(self) -> Bot:
        return self._context

    @context.setter
    def context(self, context: Bot) -> None:
        self._context = context

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def run(self):
        if self.intent == 'greeting':
            return self.action_greeting()
        if self.intent == 'weather':
            return self.action_weather()
        if self.intent == 'info':
            return self.action_info()
        if self.intent == 'exit':
            return self.action_exit()
        if self.intent == 'context':
            return self.action_set_context()

    def action_greeting(self):
        return "Hello!"

    def action_info(self):
        return "This bot can answer on question in a given context. Also it can give weather forecast"

    @abstractmethod
    def action_weather(self):
        pass

    @abstractmethod
    def action_set_context(self):
        pass

    @abstractmethod
    def action_exit(self):
        pass
