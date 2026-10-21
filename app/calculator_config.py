import os
from dotenv import load_dotenv

load_dotenv()

class CalculatorConfig:
    HISTORY_FILE = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
    LOG_FILE = os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
    MAX_HISTORY = int(os.getenv("CALCULATOR_MAX_HISTORY", "100"))