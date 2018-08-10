
from operation_types.operation import Operation
import os
import shutil
from operations.library import Library
from operation_types.operation import Operation
import inspect

class Publish(Operation):

    @staticmethod
    def name():
        return "Publish"

    @staticmethod
    def description():
        return "Publish resources files under operation"

    def _parser(self, main_parser):
        main_parser.add_argument('library',help="Library containing the operation")
        main_parser.add_argument('operation',help="Library containing the operation")
        return

    def _run(self):
        resource_dir = os.path.join(os.getcwd(),"resources")
        lib_dir = os.path.join(resource_dir,self.args.library)
        operation_dir = os.path.join(lib_dir, self.args.operation)

        for library_class in Library.__subclasses__():
            if library_class.name() == self.args.library:
                for key in library_class.operations():
                    if key == self.args.operation:
                        src = os.path.join(os.path.dirname(inspect.getfile(library_class.operations()[key])),'resources')

                        if not os.path.isdir(resource_dir):
                            os.mkdir(resource_dir)
                        if not os.path.isdir(lib_dir):
                            os.mkdir(lib_dir)

                        shutil.copytree(src,operation_dir)
                        return True
        return True
