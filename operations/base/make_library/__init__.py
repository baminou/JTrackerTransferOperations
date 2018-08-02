
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

    @staticmethod
    def parser(main_parser):
        main_parser.add_argument('name')
        return

    @staticmethod
    def _run(args):
        print(args.name)
        library_create(args.name)
        return