import json

from deeppavlov import train_model

if __name__ == '__main__':
    train_data = json.load(open("files/downloads/intent_catcher_data/train.json"))
    config = json.load(open('intent_catcher_config.json'))
    print(config)
    print(train_data)
    config['chainer']['pipe'][1]['number_of_intents'] = len(train_data.keys())
    model = train_model(config)
    print("Trained!")
