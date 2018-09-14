
from kernel.operation import Operation
import os

class Isalive(Operation):

    @staticmethod
    def name():
        return "Isalive"

    @staticmethod
    def description():
        return "Isalive has not been documented yet."

    def _parser(self, main_parser):
        main_parser.add_argument('aspera_host', help="URL of the aspera server")
        return

    def _run(self):
        response = os.system('ping -c 1 '+self.args.aspera_host)
        if response == 0:
            print(True)
            return
        print(False)