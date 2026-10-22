from app.logger import LoggingObserver
from app.auto_save_observer import AutoSaveObserver
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import History
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class Calculator:
    def __init__(self):
        self.history = History()
        self.history.load_csv(CalculatorConfig.HISTORY_FILE)
        self.observers = []
        self.add_observer(LoggingObserver())
        if CalculatorConfig.AUTO_SAVE:
            auto_save = AutoSaveObserver(CalculatorConfig.HISTORY_FILE)
            auto_save.calculations = self.history.get_history()
            self.add_observer(auto_save)

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, calculation):
        for observer in self.observers:
            observer.update(calculation)

    def calculate(self, operation_name, a, b):
        if abs(a) > CalculatorConfig.MAX_INPUT_VALUE:
            raise ValidationError("First number exceeds the maximum allowed value")

        if abs(b) > CalculatorConfig.MAX_INPUT_VALUE:
            raise ValidationError("Second number exceeds the maximum allowed value")
        operation = OperationFactory.create(operation_name)
        result = operation.execute(a, b)
        result = round(result, CalculatorConfig.PRECISION)

        calculation = Calculation(operation_name, a, b, result)
        self.history.add(calculation)
        self.notify_observers(calculation)

        return result

    def undo(self):
        self.history.undo()
        self.save_history()

    def redo(self):
        self.history.redo()
        self.save_history()
   

    def save_history(self):
        for observer in self.observers:
            if isinstance(observer, AutoSaveObserver):
                observer.save_history(self.history.get_history())

                