from app.logger import setup_logging
from app.calculator import Calculator


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

        elif command in [
            "add", "subtract", "multiply", "divide",
            "power", "root", "modulus",
            "integer_division", "percentage",
            "absolute_difference"
        ]:
            try:
                a = float(input("First number: "))
                b = float(input("Second number: "))
                result = calculator.calculate(command, a, b)
                print("Result:", result)
            except ValueError as error:
                print("Error:", error)

        else:
                print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()