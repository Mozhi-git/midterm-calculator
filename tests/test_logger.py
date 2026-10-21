import logging
from app.logger import LoggingObserver


def test_logging_observer(caplog):
    observer = LoggingObserver()

    with caplog.at_level(logging.INFO):
        observer.update("5 + 3 = 8")

    assert "New calculation: 5 + 3 = 8" in caplog.text
    