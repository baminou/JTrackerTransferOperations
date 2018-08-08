
from operation_types.yml_config_operation import YmlConfigOperation
from operation_types.json_operation import JsonOperation


class Test(YmlConfigOperation, JsonOperation):

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
        return 1
