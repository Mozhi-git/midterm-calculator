
# Midterm Calculator

## Project Description

This project is a command-line calculator application built with Python.

The calculator supports basic and advanced mathematical operations, including addition, subtraction, multiplication, division, power, root, modulus, integer division, percentage, and absolute difference.

The application also includes:

- Calculation history
- Undo and redo
- Saving and loading history using CSV files
- Automatic saving
- Logging
- Input validation and error handling
- Configuration using a .env file
- Automated testing using pytest
- GitHub Actions for continuous integration

The project uses the Factory, Memento, and Observer design patterns.


## Installation Instructions

1. Download or clone the project from GitHub.
2. Open the project folder in the terminal.
3. Create a Python virtual environment:

   python3 -m venv venv

4. Activate the virtual environment:

   source venv/bin/activate

5. Install the required packages:

   pip install -r requirements.txt

6. Start the calculator:

   python main.py


## Configuration Setup

Create a file named `.env` in the main project folder.

Add these settings:

```env
CALCULATOR_HISTORY_FILE=history.csv
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_LOG_DIR=.
CALCULATOR_HISTORY_DIR=.
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

These settings control the history file, logging, automatic saving, decimal precision, and maximum input value.

The calculator uses python-dotenv to load the settings. Logging information is saved to the configured log file.


## Usage Guide

Start the calculator by running:

    python main.py

The calculator will ask you to enter a command.

### Mathematical Commands

- add: Add two numbers.
- subtract: Subtract two numbers.
- multiply: Multiply two numbers.
- divide: Divide two numbers.
- power: Raise a number to a power.
- root: Calculate the nth root.
- modulus: Find the remainder.
- int_divide: Perform integer division.
- percent: Calculate a percentage.
- abs_diff: Calculate the absolute difference.

### Other Commands

- history: Display previous calculations.
- clear: Clear calculation history.
- undo: Undo the last calculation.
- redo: Redo the last undone calculation.
- save: Save calculation history to a CSV file.
- load: Load calculation history from a CSV file.
- help: Display available commands.
- exit: Close the calculator.

### Example

Enter command: add
First number: 5
Second number: 3
Result: 8.0

Enter command: exit
Goodbye!


## Testing Instructions

This project uses pytest for automated testing.

To run all tests:

```bash
python -m pytest tests/
```

To run tests and check code coverage:

```bash
python -m pytest tests/ --cov=app --cov=main --cov-report=term-missing --cov-fail-under=90
```

The assignment requires at least 90% test coverage.

The latest full test run passed all 94 tests with 98.88% coverage.


## CI/CD Information

This project uses GitHub Actions to automatically test the calculator.

The workflow file is located at:

`.github/workflows/python-app.yml`

When code is pushed to the main branch or a pull request is created, GitHub Actions:

1. Checks out the project code.
2. Sets up Python.
3. Installs the required dependencies.
4. Runs automated tests using pytest.
5. Checks that test coverage is at least 90%.

If the tests fail or coverage is below 90%, the workflow fails.

This helps ensure that the calculator works correctly after code changes.
