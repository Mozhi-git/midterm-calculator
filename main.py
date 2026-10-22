from app.logger import setup_logging
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from colorama import Fore, Style
from app.operations import OperationFactory

def dynamic_help(func):
    def wrapper():
        print("Available commands:")
        print(", ".join(OperationFactory.operations.keys()))
        func()
    return wrapper


@dynamic_help
def show_help():
    print("history, clear, undo, redo, save, load, help, exit")


def main():
    setup_logging()
    print("Calculator started")

    calculator = Calculator()

    while True:
        command = input("Enter command: ")

        if command == "exit":
            print("Goodbye!")
            break

        elif command == "history":
            for calc in calculator.history.get_history():
                print(calc.operation, calc.a, calc.b, "=", calc.result)

        elif command == "clear":
            calculator.history.clear()
            calculator.save_history()
            print("History cleared")

        elif command == "undo":
            calculator.undo()
            print("Undo completed")

        elif command == "redo":
            calculator.redo()
            print("Redo completed")

        elif command == "save":
            calculator.save_history()
            print("History saved")

        elif command == "load":
            try:
                calculator.history.load_csv(CalculatorConfig.HISTORY_FILE)
                print("History loaded")
            except (OSError, ValueError) as error:
                print("Error:", error)
        elif command == "help":
            show_help()

        elif command in [
            "add", "subtract", "multiply", "divide",
            "power", "root", "modulus",
            "integer_division", "percentage",
            "absolute_difference",
            "int_divide", "percent", "abs_diff"
        ]:
            try:
                a = float(input("First number: "))
                b = float(input("Second number: "))
                result = calculator.calculate(command, a, b)
                print(Fore.GREEN + f"Result: {result}" + Style.RESET_ALL)
            except ValueError as error:
                print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)

        else:
                print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()