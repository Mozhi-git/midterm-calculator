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

def test_csv_write_failure(tmp_path):
    import pytest
    from app.auto_save_observer import AutoSaveObserver

    invalid_path = tmp_path / "missing_folder" / "history.csv"
    observer = AutoSaveObserver(str(invalid_path))

    with pytest.raises(OSError, match="Unable to save calculation history"):
        observer.save_history([])