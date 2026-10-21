import pytest
from app.operations import add, subtract, multiply, divide, power, root, modulus, integer_division, percentage, absolute_difference

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



    