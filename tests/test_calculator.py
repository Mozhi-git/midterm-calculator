from unittest.mock import Mock
from app.calculator import Calculator
from app.calculation import Calculation
import pandas as pd
from app.auto_save_observer import AutoSaveObserver
from app.calculator_config import CalculatorConfig
import pytest

@pytest.fixture(autouse=True)
def clean_history(tmp_path, monkeypatch):
    filename = tmp_path / "history.csv"
    monkeypatch.setattr(CalculatorConfig, "HISTORY_FILE", str(filename))


def test_add_observer():
    calculator = Calculator()
    observer = object()

    calculator.add_observer(observer)

    assert len(calculator.observers) == 3
    assert calculator.observers[2] is observer


def test_notify_observers(tmp_path):
    calculator = Calculator()
    observer = Mock()

    calculator.add_observer(observer)

    calculation = Calculation("add", 5, 3, 8)
    calculator.notify_observers(calculation)

    observer.update.assert_called_once_with(calculation)

def test_calculate(tmp_path):
    calculator = Calculator()

    result = calculator.calculate("add", 5, 3)

    assert result == 8

def test_calculator_history():
    calculator = Calculator()

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)

    history = calculator.history.get_history()

    assert len(history) == 2
    assert history[0].result == 8
    assert history[1].result == 8
    assert history[0].operation == "add"
    assert history[1].operation == "multiply"

def test_calculator_undo():
    calculator = Calculator()

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)

    calculator.undo()

    history = calculator.history.get_history()

    assert len(history) == 1
    assert history[0].operation == "add"
    assert history[0].result == 8

def test_calculator_redo():
    calculator = Calculator()

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)

    calculator.undo()
    calculator.redo()

    history = calculator.history.get_history()

    assert len(history) == 2
    assert history[0].operation == "add"
    assert history[1].operation == "multiply"
    assert history[1].result == 8

def test_undo_updates_csv(tmp_path):
    calculator = Calculator()

    filename = tmp_path / "history.csv"

    for observer in calculator.observers:
        if isinstance(observer, AutoSaveObserver):
            observer.filename = filename

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)

    calculator.undo()

    data = pd.read_csv(filename)

    assert len(data) == 1
    assert data.iloc[0]["operation"] == "add"

def test_redo_updates_csv(tmp_path):
    calculator = Calculator()

    filename = tmp_path / "history.csv"

    for observer in calculator.observers:
        if isinstance(observer, AutoSaveObserver):
            observer.filename = filename

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)

    calculator.undo()
    calculator.redo()

    data = pd.read_csv(filename)

    assert len(data) == 2
    assert data.iloc[0]["operation"] == "add"
    assert data.iloc[1]["operation"] == "multiply"

def test_calculator_history_config():
    calculator = Calculator()

    for observer in calculator.observers:
        if isinstance(observer, AutoSaveObserver):
            assert observer.filename == CalculatorConfig.HISTORY_FILE
            return

    assert False, "AutoSaveObserver not found"

def test_history_after_restart(tmp_path, monkeypatch):
    filename = tmp_path / "history.csv"

    monkeypatch.setattr(CalculatorConfig, "HISTORY_FILE", str(filename))

    calculator1 = Calculator()
    calculator1.calculate("add", 5, 3)

    calculator2 = Calculator()
    assert len(calculator2.history.get_history()) == 1

    calculator2.calculate("multiply", 4, 2)

    calculator3 = Calculator()
    history = calculator3.history.get_history()

    assert len(history) == 2
    assert history[0].operation == "add"
    assert history[1].operation == "multiply"

def test_auto_save_disabled(tmp_path, monkeypatch):
    filename = tmp_path / "history.csv"

    monkeypatch.setattr(CalculatorConfig, "HISTORY_FILE", str(filename))
    monkeypatch.setattr(CalculatorConfig, "AUTO_SAVE", False)

    calculator = Calculator()
    calculator.calculate("add", 5, 3)

    assert len(calculator.history.get_history()) == 1
    assert not filename.exists()

def test_calculation_precision(monkeypatch):
    monkeypatch.setattr(CalculatorConfig, "PRECISION", 2)

    calculator = Calculator()
    result = calculator.calculate("divide", 10, 3)

    assert result == 3.33
    assert calculator.history.get_history()[-1].result == 3.33

def test_max_input_value(monkeypatch):
    monkeypatch.setattr(CalculatorConfig, "MAX_INPUT_VALUE", 100)

    calculator = Calculator()

    with pytest.raises(ValueError):
        calculator.calculate("add", 200, 5)

    with pytest.raises(ValueError):
        calculator.calculate("add", 5, -200)

    assert calculator.calculate("add", 50, 25) == 75

def test_nonnumeric_input():
    calculator = Calculator()

    with pytest.raises((TypeError, ValueError)):
        calculator.calculate("add", "abc", 5)