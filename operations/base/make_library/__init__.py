
from kernel.operation import Operation
import shutil
import os

class Makelibrary(Operation):

    def _schema(self):
        return {}

    @staticmethod
    def name():
        return "make_library"

    @staticmethod
    def description():
        return "Create a new library for operations"

    def _parser(self, main_parser):
        main_parser.add_argument('name')
        return

    def _run(self):
        library_name = self.args.name
        library_template_path = os.path.join(os.path.dirname(os.path.relpath(__file__)),'resources','template')
        library_new_path = os.path.join('operations',str(library_name).lower())
        library_new_init = os.path.join(library_new_path,'__init__.py')
        shutil.copytree(library_template_path,library_new_path)

        with open(library_new_init,'r') as f:
            new_text = f.read().replace('LIBRARYNAME', str(library_name).lower())

        with open(library_new_init,'w') as f:
            f.write(new_text)
        return