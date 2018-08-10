
from operation_types.operation import Operation
from operations.library import Library

class Install(Operation):

    @staticmethod
    def name():
        return "Install"

    @staticmethod
    def description():
        return "Install has not been documented yet."

    def _parser(self, main_parser):
        return

    def _run(self):
        for library_class in Library.__subclasses__():
            for key in library_class.operations():
                print(library_class.name() + " - "+key)
                library_class.operations()[key].install()
        return True