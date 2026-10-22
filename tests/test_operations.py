import pytest
from app.operations import add, subtract, multiply, divide, power, root, modulus, integer_division, percentage, absolute_difference
from app.operations import Addition, Subtraction, Multiplication, Division, Power, Root, Modulus, IntegerDivision, Percentage, AbsoluteDifference
from app.operations import OperationFactory
from app.exceptions import OperationError

def test_add():
    assert add(5, 3) == 8

def test_subtract():
    assert subtract(10, 4) == 6

def test_multiply():
    assert multiply(5, 3) == 15

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_power():
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(2, -1) == 0.5

def test_root():
    assert root(25, 2) == 5
    assert root(27, 3) == pytest.approx(3)
    assert root(-27, 3) == pytest.approx(-3)


def test_root_zero_degree():
    with pytest.raises(ValueError):
        root(25, 0)


def test_root_negative_even():
    with pytest.raises(ValueError):
        root(-16, 2)

def test_modulus():
    assert modulus(10, 3) == 1
    assert modulus(15, 4) == 3
    assert modulus(20, 5) == 0


def test_modulus_by_zero():
    with pytest.raises(ValueError):
        modulus(10, 0)

def test_integer_division():
    assert integer_division(10, 3) == 3
    assert integer_division(20, 4) == 5
    assert integer_division(-10, 3) == -4


def test_integer_division_by_zero():
    with pytest.raises(ValueError):
        integer_division(10, 0)

def test_percentage():
    assert percentage(25, 100) == 25
    assert percentage(50, 200) == 25
    assert percentage(75, 100) == 75


def test_percentage_by_zero():
    with pytest.raises(ValueError):
        percentage(25, 0)

def test_absolute_difference():
    assert absolute_difference(10, 4) == 6
    assert absolute_difference(4, 10) == 6
    assert absolute_difference(5, 5) == 0

def test_addition_class():
    operation = Addition()
    assert operation.execute(5, 3) == 8

def test_subtraction_class():
    operation = Subtraction()
    assert operation.execute(10, 4) == 6

def test_multiplication_class():
    operation = Multiplication()
    assert operation.execute(5, 3) == 15

def test_division_class():
    operation = Division()
    assert operation.execute(10, 2) == 5


def test_division_class_by_zero():
    operation = Division()
    with pytest.raises(ValueError):
        operation.execute(10, 0)

def test_power_class():
    operation = Power()
    assert operation.execute(2, 3) == 8
    assert operation.execute(2, -1) == 0.5

def test_root_class():
    operation = Root()
    assert operation.execute(25, 2) == 5
    assert operation.execute(27, 3) == pytest.approx(3)
    assert operation.execute(-27, 3) == pytest.approx(-3)

def test_modulus_class():
    operation = Modulus()
    assert operation.execute(10, 3) == 1
    assert operation.execute(20, 5) == 0


def test_modulus_class_by_zero():
    operation = Modulus()
    with pytest.raises(ValueError):
        operation.execute(10, 0)

def test_integer_division_class():
    operation = IntegerDivision()
    assert operation.execute(10, 3) == 3
    assert operation.execute(-10, 3) == -4


def test_integer_division_class_by_zero():
    operation = IntegerDivision()
    with pytest.raises(ValueError):
        operation.execute(10, 0)

def test_percentage_class():
    operation = Percentage()
    assert operation.execute(25, 100) == 25
    assert operation.execute(50, 200) == 25


def test_percentage_class_by_zero():
    operation = Percentage()
    with pytest.raises(ValueError):
        operation.execute(25, 0)

def test_absolute_difference_class():
    operation = AbsoluteDifference()
    assert operation.execute(10, 4) == 6
    assert operation.execute(4, 10) == 6
    assert operation.execute(5, 5) == 0

def test_factory():
    operation = OperationFactory.create("add")
    assert isinstance(operation, Addition)
    assert operation.execute(5, 3) == 8


def test_factory_invalid():
    with pytest.raises(ValueError):
        OperationFactory.create("unknown")

@pytest.mark.parametrize("name, expected_class", [
    ("add", Addition),
    ("subtract", Subtraction),
    ("multiply", Multiplication),
    ("divide", Division),
    ("power", Power),
    ("root", Root),
    ("modulus", Modulus),
    ("integer_division", IntegerDivision),
    ("percentage", Percentage),
    ("absolute_difference", AbsoluteDifference),
])
def test_factory_all_operations(name, expected_class):
    operation = OperationFactory.create(name)
    assert isinstance(operation, expected_class)

def test_custom_operation_error():
    with pytest.raises(OperationError):
        OperationFactory.create("unknown")


    