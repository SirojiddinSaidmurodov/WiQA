import json

from deeppavlov import train_model

train_data = json.load(open("files/downloads/intent_catcher_data/train.json"))
config = json.load(open('intent_catcher_config.json'))
print(config)
print(train_data)
config['chainer']['pipe'][1]['number_of_intents'] = len(train_data.keys())
config['train']['epochs'] = 40
model = train_model(config)
print("Trained!")
