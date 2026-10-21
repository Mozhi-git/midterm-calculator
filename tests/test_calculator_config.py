from app.calculator_config import CalculatorConfig


def test_calculator_config():
    assert CalculatorConfig.HISTORY_FILE == "history.csv"
    assert CalculatorConfig.LOG_FILE == "calculator.log"
    assert CalculatorConfig.MAX_HISTORY == 100