from app.calculator_memento import CalculatorMemento
class History:
    def __init__(self):
        self.calculations = []
        self.undo_stack = []
        self.redo_stack = []

    def add(self, calculation):
        self.undo_stack.append(CalculatorMemento(self.calculations))
        self.calculations.append(calculation)
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