from app.calculator_memento import CalculatorMemento


def test_memento():
    calculations = [1, 2, 3]

    memento = CalculatorMemento(calculations)

    calculations.append(4)

    assert memento.calculations == [1, 2, 3]