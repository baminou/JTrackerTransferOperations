
from operation_types.operation import Operation

class NEWOPERATION(Operation):

    @staticmethod
    def name():
        return "NEWOPERATION"

    @staticmethod
    def description():
        return "NEWOPERATION has not been documented yet."

    def _parser(self, main_parser):
        return

    def _run(self):
        raise NotImplementedError("NEWOPERATION not implemented yet.")