
from operation_types.operation import Operation
import pip
import os
from operations.library import Library
import inspect

class Installoperation(Operation):

    @staticmethod
    def name():
        return "install_operation"

    @staticmethod
    def description():
        return "Install requirements for the operation using requirements.txt"

    def _parser(self, main_parser):
        main_parser.add_argument('library')
        main_parser.add_argument('operation')
        return

    def _run(self):
        for library_class in Library.__subclasses__():
            if library_class.name() == self.args.library:
                for key in library_class.operations():
                    if library_class.operations()[key].name() == self.args.operation:
                        library_class.operations()[key].install()
                        return True
        return True
