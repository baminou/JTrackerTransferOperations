
from operation_types.operation import Operation
from operations.library import Library

class Installlibrary(Operation):

    @staticmethod
    def name():
        return "install_library"

    @staticmethod
    def description():
        return "Installlibrary has not been documented yet."

    def _parser(self, main_parser):
        main_parser.add_argument('library')
        return

    def _run(self):
        for library_class in Library.__subclasses__():
            if library_class.name() == self.args.library:
                for key in library_class.operations():
                    print(key)
                    library_class.operations()[key].install()
        return True