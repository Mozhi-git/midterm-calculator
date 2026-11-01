import pandas as pd


class AutoSaveObserver:
    def __init__(self, filename="history.csv"):
        self.filename = filename
        self.calculations = []

    def update(self, calculation):
        self.calculations.append(calculation)
        self.save_history(self.calculations)
       

    def save_history(self, calculations):
        self.calculations = calculations.copy()

        data = [
            {
                "operation": calc.operation,
                "a": calc.a,
                "b": calc.b,
                "result": calc.result,
                "timestamp": calc.timestamp
            }
            for calc in self.calculations
        ]

        try:
            pd.DataFrame(
                data,
                columns=["operation", "a", "b", "result", "timestamp"]
            ).to_csv(self.filename, index=False)
        except OSError as error:
            raise OSError(
                f"Unable to save calculation history to {self.filename}: {error}"
            ) from error