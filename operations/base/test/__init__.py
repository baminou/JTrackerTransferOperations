
from operations.yml_config_operation import YmlConfigOperation
import time

class Test(YmlConfigOperation):

    @staticmethod
    def name():
        return "Test"

    @staticmethod
    def description():
        return "Test has not been documented yet."

    def _config_schema(self):
        return {}

    def _parser(self, main_parser):
        return

    def _run(self):
        print(self.args.config.readlines())
        return 1
