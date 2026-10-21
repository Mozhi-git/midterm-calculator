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