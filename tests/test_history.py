from app.history import History
from app.calculation import Calculation


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