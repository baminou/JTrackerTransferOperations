
from operation_types.operation import Operation

class Uploadsongpayload(Operation):

    @staticmethod
    def name():
        return "Uploadsongpayload"

    @staticmethod
    def description():
        return "Uploadsongpayload has not been documented yet."

    def _parser(self, main_parser):
        return

    def _run(self):
        raise NotImplementedError("Uploadsongpayload not implemented yet.")