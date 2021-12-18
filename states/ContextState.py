import json

import wikipedia as wiki

from UserProperties import UserProperties
from states.AbstractState import AbstractState
from states.QuestionAnsweringState import QAState
from states.StartState import StartState


class ContextState(AbstractState):

    def run(self):
        message: str = self.message.text[1:2]
        if message.isnumeric():
            user: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
            results: dict = json.loads(user.searchResults)
            user.context = str(wiki.page(results.get(int(message))))
            user.save()
            self.context.set_state(QAState(self.message, self.intent))
            return "Context set"
        else:
            if self.intent == "exit":
                self.action_exit()
            return "Try again"

    @property
    def name(self) -> str:
        return "context"

    def action_weather(self):
        pass

    def action_set_context(self):
        pass

    def action_exit(self):
        self.context.set_state(StartState(self.message, self.intent))
        return "State is reset"
