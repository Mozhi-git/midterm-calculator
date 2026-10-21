import pandas as pd

from app.auto_save_observer import AutoSaveObserver
from app.calculation import Calculation


def test_auto_save_observer(tmp_path):
    filename = tmp_path / "history.csv"
    observer = AutoSaveObserver(filename)

    calc = Calculation("add", 5, 3, 8)
    observer.update(calc)

    assert filename.exists()

    data = pd.read_csv(filename)

    assert len(data) == 1
    assert data.iloc[0]["operation"] == "add"
    assert data.iloc[0]["result"] == 8

def test_save_history(tmp_path):
    filename = tmp_path / "history.csv"
    observer = AutoSaveObserver(filename)

    calc1 = Calculation("add", 5, 3, 8)
    calc2 = Calculation("multiply", 4, 2, 8)

    observer.save_history([calc1, calc2])

    data = pd.read_csv(filename)
    assert len(data) == 2

    observer.save_history([calc1])

    data = pd.read_csv(filename)
    assert len(data) == 1
    assert data.iloc[0]["operation"] == "add"