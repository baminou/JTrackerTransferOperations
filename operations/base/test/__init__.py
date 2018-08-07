
from operations.operation import Operation
import time

class Test(Operation):

    @staticmethod
    def name():
        return "Test"

    @staticmethod
    def description():
        return "Test has not been documented yet."

    @staticmethod
    def parser(main_parser):
        return

    def _run(self, args):
        print("start")
        time.sleep(2)
        print("end")
