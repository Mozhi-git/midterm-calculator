from app.history import History
from app.calculation import Calculation
import pandas as pd
from datetime import datetime
from app.calculator_config import CalculatorConfig



def test_history():
    history = History()

    calc = Calculation("add", 5, 3, 8)
    history.add(calc)

    saved = history.get_history()

    assert len(saved) == 1
    assert saved[0].result == 8

def test_clear_history():
    history = History()

    calc = Calculation("add", 5, 3, 8)
    history.add(calc)

    history.clear()

    assert len(history.get_history()) == 0

def test_history_snapshot():
    history = History()

    calc = Calculation("add", 5, 3, 8)
    history.add(calc)

    assert len(history.undo_stack) == 1
    assert history.undo_stack[0].calculations == []
    assert len(history.get_history()) == 1

def test_undo():
    history = History()

    calc1 = Calculation("add", 5, 3, 8)
    calc2 = Calculation("subtract", 10, 4, 6)

    history.add(calc1)
    history.add(calc2)

    history.undo()

    assert len(history.get_history()) == 1
    assert history.get_history()[0].result == 8
    assert len(history.redo_stack) == 1

def test_redo():
    history = History()

    calc1 = Calculation("add", 5, 3, 8)
    calc2 = Calculation("subtract", 10, 4, 6)

    history.add(calc1)
    history.add(calc2)

    history.undo()
    history.redo()

    assert len(history.get_history()) == 2
    assert history.get_history()[0].result == 8
    assert history.get_history()[1].result == 6

def test_undo_empty_history():
    history = History()

    history.undo()

    assert history.get_history() == []

def test_redo_empty_history():
    history = History()

    history.redo()

    assert history.get_history() == []

def test_redo_cleared_after_new_calculation():
    history = History()

    calc1 = Calculation("add", 5, 3, 8)
    calc2 = Calculation("subtract", 10, 4, 6)
    calc3 = Calculation("multiply", 2, 3, 6)

    history.add(calc1)
    history.add(calc2)

    history.undo()
    history.add(calc3)

    assert len(history.redo_stack) == 0
    assert history.get_history() == [calc1, calc3]

def test_clear_history_stacks():
    history = History()

    calc1 = Calculation("add", 5, 3, 8)
    calc2 = Calculation("subtract", 10, 4, 6)

    history.add(calc1)
    history.add(calc2)
    history.undo()
    history.clear()

    assert history.get_history() == []
    assert history.undo_stack == []
    assert history.redo_stack == []

def test_load_csv(tmp_path):
    filename = tmp_path / "history.csv"

    data = pd.DataFrame([
        {"operation": "add", "a": 5, "b": 3, "result": 8},
        {"operation": "multiply", "a": 4, "b": 2, "result": 8}
    ])

    data.to_csv(filename, index=False)

    history = History()
    history.load_csv(filename)

    saved = history.get_history()

    assert len(saved) == 2
    assert saved[0].operation == "add"
    assert saved[0].result == 8
    assert saved[1].operation == "multiply"
    assert saved[1].result == 8

def test_load_missing_csv(tmp_path):
    filename = tmp_path / "missing.csv"

    history = History()
    history.load_csv(filename)

    assert history.get_history() == []

def test_load_empty_csv(tmp_path):
    filename = tmp_path / "empty.csv"
    filename.touch()

    history = History()
    history.load_csv(filename)

    assert history.get_history() == []

def test_load_csv_timestamp(tmp_path):
    filename = tmp_path / "history.csv"

    original = datetime(2026, 1, 15, 10, 30)

    data = pd.DataFrame([{
        "operation": "add",
        "a": 5,
        "b": 3,
        "result": 8,
        "timestamp": original
    }])

    data.to_csv(filename, index=False)

    history = History()
    history.load_csv(filename)

    saved = history.get_history()

    assert len(saved) == 1
    assert saved[0].timestamp == original

def test_max_history(monkeypatch):
    monkeypatch.setattr(CalculatorConfig, "MAX_HISTORY", 3)

    history = History()

    for i in range(5):
        calc = Calculation("add", i, 1, i + 1)
        history.add(calc)

    saved = history.get_history()

    assert len(saved) == 3
    assert saved[0].a == 2
    assert saved[1].a == 3
    assert saved[2].a == 4 

def test_load_csv_max_history(tmp_path, monkeypatch):
    monkeypatch.setattr(CalculatorConfig, "MAX_HISTORY", 3)

    filename = tmp_path / "history.csv"

    data = pd.DataFrame([
        {"operation": "add", "a": i, "b": 1, "result": i + 1}
        for i in range(5)
    ])

    data.to_csv(filename, index=False)

    history = History()
    history.load_csv(filename)

    saved = history.get_history()

    assert len(saved) == 3
    assert [calc.a for calc in saved] == [2, 3, 4]

def test_undo_max_history(monkeypatch):
    monkeypatch.setattr(CalculatorConfig, "MAX_HISTORY", 3)

    history = History()

    for i in range(4):
        calc = Calculation("add", i, 1, i + 1)
        history.add(calc)

    assert len(history.get_history()) == 3

    history.undo()

    assert len(history.get_history()) == 3
    assert [calc.a for calc in history.get_history()] == [0, 1, 2]

def test_redo_max_history(monkeypatch):
    monkeypatch.setattr(CalculatorConfig, "MAX_HISTORY", 3)

    history = History()

    for i in range(4):
        calc = Calculation("add", i, 1, i + 1)
        history.add(calc)

    history.undo()
    history.redo()

    saved = history.get_history()

    assert len(saved) == 3
    assert [calc.a for calc in saved] == [1, 2, 3]

def test_load_twice_no_duplicates(tmp_path):
    import pandas as pd

    filename = tmp_path / "history.csv"
    pd.DataFrame([
        {"operation": "add", "a": 5, "b": 3, "result": 8}
    ]).to_csv(filename, index=False)

    history = History()
    history.load_csv(filename)
    history.load_csv(filename)

    assert len(history.get_history()) == 1