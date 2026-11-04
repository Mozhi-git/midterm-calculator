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


def test_repl_continues_after_save_error(monkeypatch, capsys, tmp_path):
    from app.calculator_config import CalculatorConfig

    monkeypatch.setattr(
        CalculatorConfig, "HISTORY_FILE", str(tmp_path / "history.csv")
    )
    monkeypatch.setattr(CalculatorConfig, "AUTO_SAVE", False)

    inputs = iter(["save", "add", "5", "3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"), patch(
        "main.Calculator.save_history",
        side_effect=OSError("Disk full")
    ):
        main()

    captured = capsys.readouterr()

    assert "Unable to save history" in captured.out
    assert "Result: 8.0" in captured.out
    assert "Goodbye!" in captured.out

def test_repl_continues_after_autosave_error(monkeypatch, capsys, tmp_path):
    from app.calculator_config import CalculatorConfig

    monkeypatch.setattr(
        CalculatorConfig, "HISTORY_FILE", str(tmp_path / "history.csv")
    )
    monkeypatch.setattr(CalculatorConfig, "AUTO_SAVE", True)

    inputs = iter([
        "add", "5", "3",
        "add", "10", "2",
        "exit"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"), patch(
        "app.auto_save_observer.AutoSaveObserver.save_history",
        side_effect=[OSError("Disk full"), None]
    ):
        main()

    captured = capsys.readouterr()

    assert "Error:" in captured.out
    assert "Disk full" in captured.out
    assert "Result: 12.0" in captured.out
    assert "Goodbye!" in captured.out


def test_repl_recovers_from_clear_undo_redo_errors(monkeypatch, capsys, tmp_path):
    from app.calculator_config import CalculatorConfig

    monkeypatch.setattr(
        CalculatorConfig, "HISTORY_FILE", str(tmp_path / "history.csv")
    )
    monkeypatch.setattr(CalculatorConfig, "AUTO_SAVE", False)

    inputs = iter([
        "add", "5", "3",
        "undo",
        "redo",
        "clear",
        "add", "2", "3",
        "exit"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("main.setup_logging"), patch(
        "main.Calculator.save_history",
        side_effect=OSError("Disk full")
    ):
        main()

    output = capsys.readouterr().out

    assert "Unable to save history after undo" in output
    assert "Unable to save history after redo" in output
    assert "History cleared, but unable to save" in output
    assert "Result: 5.0" in output
    assert "Goodbye!" in output
