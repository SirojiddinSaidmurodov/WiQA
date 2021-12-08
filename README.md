# WiQA
Telegram bot for answering the questions over passed text.
### Running:
Use python 3.7

```shell
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python3 -m deeppavlov install squad_bert
python3 -m deeppavlov install intent_catcher
python3 train_intent_cathcher.py
python3 UserProperties.py
python3 bot.py
```
