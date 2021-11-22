class ArgsDto:
    def __init__(self, intent_catcher, context_qa, message):
        self.intent_catcher = intent_catcher
        self.context_qa = context_qa
        self.message = message
