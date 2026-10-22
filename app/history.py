from app.calculator_memento import CalculatorMemento
import pandas as pd
from app.calculation import Calculation
from pathlib import Path
from app.calculator_config import CalculatorConfig

class History:
    def __init__(self):
        self.calculations = []
        self.undo_stack = []
        self.redo_stack = []

    def add(self, calculation):
        self.undo_stack.append(CalculatorMemento(self.calculations))
        self.calculations.append(calculation)

        if len(self.calculations) > CalculatorConfig.MAX_HISTORY:
            self.calculations.pop(0)

        self.redo_stack.clear()

    def get_history(self):
        return self.calculations.copy()

    def clear(self):
        self.calculations.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return

        self.redo_stack.append(CalculatorMemento(self.calculations))
        memento = self.undo_stack.pop()
        self.calculations = memento.calculations.copy()

    def redo(self):
        if not self.redo_stack:
            return

        self.undo_stack.append(CalculatorMemento(self.calculations))
        memento = self.redo_stack.pop()
        self.calculations = memento.calculations.copy()

    def load_csv(self, filename):
        if not Path(filename).exists():
            return
        try:
            data = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            return

        self.calculations = []

        for _, row in data.iterrows():
            calculation = Calculation(
                row["operation"],
                row["a"],
                row["b"],
                row["result"]
            )

            if "timestamp" in data.columns and pd.notna(row["timestamp"]):
                calculation.timestamp = pd.to_datetime(
                    row["timestamp"]
                ).to_pydatetime()


            self.calculations.append(calculation)

            if len(self.calculations) > CalculatorConfig.MAX_HISTORY:
                self.calculations.pop(0)

        self.undo_stack.clear()
        self.redo_stack.clear()

