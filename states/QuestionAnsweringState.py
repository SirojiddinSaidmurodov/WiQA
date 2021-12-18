from UserProperties import UserProperties
from run import context_qa_model
from states.AbstractState import AbstractState
from states.StartState import StartState


class QAState(AbstractState):

    def run(self):
        if self.intent == "exit":
            self.action_exit()
        user: UserProperties = UserProperties.get_by_id(self.message.from_user.id)
        return context_qa_model(user.context, [self.message.text])

    @property
    def name(self) -> str:
        return "QA"

    def action_weather(self):
        pass

    def action_set_context(self):
        pass

    def action_exit(self):
        self.context.set_state(StartState(self.message, self.intent))
        return "State reset"
