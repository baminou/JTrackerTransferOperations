
from operation_types.operation import Operation
from operations.library import Library
import subprocess

class Install(Operation):

    @staticmethod
    def name():
        return "Install"

    @staticmethod
    def description():
        return "Install has not been documented yet."

    def _parser(self, main_parser):
        main_parser.add_argument('pip_version',help="Command of pip to run for packages eg. pip, pip3, ...")
        return

    def _run(self):
        try:
            subprocess.check_output(['pipreqs', '.'])
        except OSError as e:
            raise Exception("Install pipreqs, run: pip install pipreqs")

        try:
            subprocess.check_output([self.args.pip_version, 'install', '-r', 'requirements.txt'])
        except OSError as e:
            raise Exception("Program missing, install %s" % (self.args.pip_version))


        return True