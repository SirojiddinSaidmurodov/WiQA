import logging

import rpyc
from deeppavlov import build_model

logging.basicConfig(level=logging.DEBUG)
intent_catcher_model = build_model('intent_catcher_config.json')


class CalculatorService(rpyc.Service):
    def exposed_get_intent(self, message):
        intent = intent_catcher_model([message])[0]
        logging.debug(intent)
        return intent


if __name__ == "__main__":
    from rpyc.utils.server import OneShotServer

    logging.debug("Running...")
    t = OneShotServer(CalculatorService, port=18861)
    t.start()
