import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class CalculatorConfig:
    HISTORY_FILE = str(
    Path(os.getenv("CALCULATOR_HISTORY_DIR", ".")) /
    os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
)
    LOG_FILE = str(
        Path(os.getenv("CALCULATOR_LOG_DIR", ".")) /
        os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
    )
    MAX_HISTORY = MAX_HISTORY_SIZE = int(
    os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
)



    LOG_DIR = os.getenv("CALCULATOR_LOG_DIR", ".")
    HISTORY_DIR = os.getenv("CALCULATOR_HISTORY_DIR", ".")
    AUTO_SAVE = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
    PRECISION = int(os.getenv("CALCULATOR_PRECISION", "2"))
    MAX_INPUT_VALUE = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000"))
    DEFAULT_ENCODING = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")


    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    Path(HISTORY_DIR).mkdir(parents=True, exist_ok=True)