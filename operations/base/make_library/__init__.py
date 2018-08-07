
from operations.operation import Operation
from ..utils import library_create

class Makelibrary(Operation):

    def _schema(self):
        return {}

    @staticmethod
    def name():
        return "make_library"

    @staticmethod
    def description():
        return "Create a new library"

    def _parser(self, main_parser):
        main_parser.add_argument('name')
        return

    def _run(self, args):
        library_create(args.name)
        return