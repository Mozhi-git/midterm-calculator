from app.calculator_config import CalculatorConfig


def test_calculator_config():
    assert CalculatorConfig.HISTORY_FILE == "history.csv"
    assert CalculatorConfig.LOG_FILE == "calculator.log"
    assert CalculatorConfig.MAX_HISTORY == 100

def test_required_config():
    assert CalculatorConfig.LOG_DIR == "."
    assert CalculatorConfig.HISTORY_DIR == "."
    assert CalculatorConfig.MAX_HISTORY_SIZE == 100
    assert CalculatorConfig.AUTO_SAVE is True
    assert CalculatorConfig.PRECISION == 2
    assert CalculatorConfig.MAX_INPUT_VALUE == 1000000
    assert CalculatorConfig.DEFAULT_ENCODING == "utf-8"