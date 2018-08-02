
from operations.operation import Operation

class NEWOPERATION(Operation):

    @staticmethod
    def name():
        return "NEWOPERATION"

    @staticmethod
    def description():
        return "NEWOPERATION has not been documented yet."

    @staticmethod
    def parser(main_parser):
        return

    @staticmethod
    def _run(args):
        raise NotImplementedError("NEWOPERATION not implemented yet.")