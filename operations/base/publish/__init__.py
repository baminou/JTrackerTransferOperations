
from operation_types.operation import Operation
import os
import shutil

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

        if not os.path.isdir(resource_dir):
            os.mkdir(resource_dir)
        if not os.path.isdir(lib_dir):
            os.mkdir(lib_dir)

        shutil.copytree(os.path.join(os.getcwd(),'operations',self.args.library,self.args.operation,'resources'),operation_dir)

