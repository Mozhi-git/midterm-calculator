import logging


class LoggingObserver:
    def update(self, calculation):
        logging.info("New calculation: %s", calculation)