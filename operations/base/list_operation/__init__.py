
from operation_types.operation import Operation
from operations.library import Library
import inspect
from termcolor import colored
import tabulate


class Listoperation(Operation):

    @staticmethod
    def name():
        return "list_operation"

    @staticmethod
    def description():
        return "List all operations"

    def _parser(self, main_parser):
        main_parser.add_argument('-l', '--library', dest='library', required=False)
        return

    def _run(self):
        headers = ['Library', 'Command', 'Operation', 'Description']
        data = []
        for library_class in Library.__subclasses__():
            if self.args.library and not self.args.library == library_class.name():
                continue
            for operation_key, operation in library_class.operations().items():
                color = "red"
                try:
                    inspect.getfile(operation)
                    color = "green"
                except TypeError:
                    pass

                data.append([colored(library_class.name(),'blue'), colored(operation_key, color), operation.name(), operation.description()[:50]])
        print(tabulate.tabulate(data,headers))
        return True
