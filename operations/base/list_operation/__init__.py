
from operation_types.operation import Operation
from operations.library import Library
import inspect
from termcolor import colored
import tabulate


class Listoperation(Operation):

    @staticmethod
    def name():
        return "Listoperation"

    @staticmethod
    def description():
        return "List all operations"

    def _parser(self, main_parser):
        return

    def _run(self):
        headers = ['Library', 'Operation', 'Command', 'Description']
        data = []
        for library_class in Library.__subclasses__():
            for operation_key, operation in library_class.operations().items():
                color = "red"
                try:
                    inspect.getfile(operation)
                    color = "green"
                except TypeError:
                    pass

                data.append([colored(library_class.name(),'blue'), colored(operation_key, color), operation.name(), operation.description()[:50]])
        print(tabulate.tabulate(data,headers))
        return
