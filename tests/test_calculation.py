from datetime import datetime
from app.calculation import Calculation


def test_calculation():
    calc = Calculation("add", 5, 3, 8)

    assert calc.operation == "add"
    assert calc.a == 5
    assert calc.b == 3
    assert calc.result == 8
    assert isinstance(calc.timestamp, datetime)