from deeppavlov import build_model

intent_catcher_model = build_model('intent_catcher_config.json')
context_qa_model = build_model('contextQAConfig.json')
