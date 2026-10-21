from app.logger import LoggingObserver
from app.auto_save_observer import AutoSaveObserver
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import History


class Calculator:
    def __init__(self):
        self.history = History()
        self.observers = []
        self.add_observer(LoggingObserver())
        self.add_observer(AutoSaveObserver())

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, calculation):
        for observer in self.observers:
            observer.update(calculation)

    def calculate(self, operation_name, a, b):
        operation = OperationFactory.create(operation_name)
        result = operation.execute(a, b)

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