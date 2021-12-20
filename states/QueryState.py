import json
import logging

import wikipedia as wiki

from states.AbstractState import AbstractState


class QueryState(AbstractState):
    @property
    def name(self) -> str:
        return 'query'

    def run(self):
        results = wiki.search(self.message.text)
        answer_message = ''
        results_map = dict()
        for i, result in zip(range(len(results)), results):
            answer_message += f"/{i} {result}\n"
            results_map[i] = result
        self.context.set_state(ContextState(self.message, self.intent))
        properties: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
        properties.searchResults = json.dumps(results_map)
        logging.debug(properties.searchResults)
        logging.debug(json.dumps(results_map))
        properties.save()
        return "Choose an article for setting as context: \n" + answer_message

    def action_weather(self):
        pass

    def action_set_context(self):
        pass

    def action_exit(self):
        pass


from states.ContextState import ContextState
from UserProperties import UserProperties
