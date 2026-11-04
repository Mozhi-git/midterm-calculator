from app.calculator_config import CalculatorConfig
import os
import subprocess
import sys


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

def test_invalid_precision_falls_back_to_default():
    for invalid_value in ("abc", "-5"):
        env = os.environ.copy()
        env["CALCULATOR_PRECISION"] = invalid_value

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from app.calculator_config import CalculatorConfig; "
                "print(CalculatorConfig.PRECISION)",
            ],
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.stdout.strip() == "2"


def test_invalid_startup_settings_use_defaults():
    settings = [
        ("CALCULATOR_MAX_HISTORY_SIZE", "MAX_HISTORY", "100"),
        ("CALCULATOR_MAX_INPUT_VALUE", "MAX_INPUT_VALUE", "1000000.0"),
    ]

    for variable, attribute, expected in settings:
        for invalid_value in ("abc", "-5", "0", "nan"):
            env = os.environ.copy()
            env[variable] = invalid_value

            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"from app.calculator_config import CalculatorConfig; "
                    f"print(CalculatorConfig.{attribute})",
                ],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

            assert result.stdout.strip() == expected
