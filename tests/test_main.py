from unittest.mock import patch
from main import main


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "exit")

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Calculator started" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_add(monkeypatch, capsys):
    inputs = iter(["add", "5", "3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Result: 8.0" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_invalid_input(monkeypatch, capsys):
    inputs = iter(["add", "abc", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Error:" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_history(monkeypatch, capsys):
    inputs = iter(["add", "5", "3", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Result: 8.0" in captured.out
    assert "add 5.0 3.0 = 8.0" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_clear(monkeypatch, capsys):
    inputs = iter(["add", "5", "3", "clear", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Result: 8.0" in captured.out
    assert "History cleared" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_undo_redo(monkeypatch, capsys):
    inputs = iter([
        "add", "5", "3",
        "multiply", "4", "2",
        "undo",
        "redo",
        "history",
        "exit"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Undo completed" in captured.out
    assert "Redo completed" in captured.out
    assert "add 5.0 3.0 = 8.0" in captured.out
    assert "multiply 4.0 2.0 = 8.0" in captured.out

def test_repl_unknown_command(monkeypatch, capsys):
    inputs = iter(["hello", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Unknown command. Please try again." in captured.out
    assert "Goodbye!" in captured.out

def test_repl_division_by_zero(monkeypatch, capsys):
    inputs = iter([
        "divide", "10", "0",
        "add", "5", "3",
        "exit"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Error: Cannot divide by zero" in captured.out
    assert "Result: 8.0" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_help(monkeypatch, capsys):
    inputs = iter(["help", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "Available commands:" in captured.out
    assert "int_divide" in captured.out
    assert "percent" in captured.out
    assert "abs_diff" in captured.out

def test_repl_save(monkeypatch, capsys, tmp_path):
    from app.calculator_config import CalculatorConfig

    filename = tmp_path / "history.csv"
    monkeypatch.setattr(CalculatorConfig, "HISTORY_FILE", str(filename))

    inputs = iter(["add", "5", "3", "save", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "History saved" in captured.out
    assert filename.exists()

def test_repl_load(monkeypatch, capsys, tmp_path):
    from app.calculator_config import CalculatorConfig
    from app.calculation import Calculation
    from app.history import History
    from app.calculator import Calculator

    filename = tmp_path / "history.csv"
    monkeypatch.setattr(CalculatorConfig, "HISTORY_FILE", str(filename))

    calculator = Calculator()
    calculator.calculate("add", 5, 3)
    calculator.save_history()

    inputs = iter(["load", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"):
        main()

    captured = capsys.readouterr()

    assert "History loaded" in captured.out
    assert "add 5" in captured.out

def test_dynamic_help(monkeypatch, capsys):
    from main import show_help
    from app.operations import OperationFactory

    monkeypatch.setitem(
        OperationFactory.operations,
        "test_operation",
        object
    )

    show_help()
    captured = capsys.readouterr()

    assert "test_operation" in captured.out