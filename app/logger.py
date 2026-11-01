import logging
from app.calculator_config import CalculatorConfig

def setup_logging():
    try:
        logging.basicConfig(
            filename=CalculatorConfig.LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True
        )
    except OSError:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True
        )


class LoggingObserver:
    def update(self, calculation):
        logging.info("New calculation: %s", calculation)