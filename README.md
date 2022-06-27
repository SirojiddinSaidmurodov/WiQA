# WiQA
Telegram bot for answering the questions over passed text.
### Running:
In order to connect to the Telegram and OpenWeatherMap, create `.env` file in the root file with params `bot_token` standing for Telegram bot token and `owm_token` with OWM API key.
```dotenv
# This keys are only for reference, they are not valid 😀
bot_token=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
owm_token=l3gxyyktcbrxy1reqmtkdj46hszkmucr
```

❗️Use python 3.7
```shell
# Create and activate virtual environment
python -m venv .venv
.venv/Scripts/activate
# Install dependencies
pip install -r requirements.txt
python3 -m deeppavlov install squad_bert
python3 -m deeppavlov install intent_catcher

# Train intent catcher model
python3 train_intent_cathcher.py

# Create database
python3 UserProperties.py

# Before running bot, you need to have running intent catcher server
python3 intent_catcher_server.py
# Run the main script in other shell
python3 run.py
```
