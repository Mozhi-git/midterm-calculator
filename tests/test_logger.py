import logging
from app.logger import LoggingObserver, setup_logging
from app.calculator_config import CalculatorConfig


def test_logging_observer(caplog):
    observer = LoggingObserver()

    with caplog.at_level(logging.INFO):
        observer.update("5 + 3 = 8")

    assert "New calculation: 5 + 3 = 8" in caplog.text

def test_setup_logging(tmp_path, monkeypatch):
    filename = tmp_path / "calculator.log"

    monkeypatch.setattr(CalculatorConfig, "LOG_FILE", str(filename))

    setup_logging()
    logging.info("Test calculation")

    assert filename.exists()
    assert "Test calculation" in filename.read_text()

    logging.shutdown()

def test_logging_fallback(monkeypatch):
    import logging
    from app.logger import setup_logging

    original_basic_config = logging.basicConfig
    attempts = []

    def fake_basic_config(**kwargs):
        attempts.append(kwargs)

        if "filename" in kwargs:
            raise OSError("Cannot write log file")

        return original_basic_config(**kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

    setup_logging()

    assert len(attempts) == 2
    assert "filename" in attempts[0]
    assert "filename" not in attempts[1]
