
from operation_types.command_operation import CommandOperation

class Upload(CommandOperation):

    @staticmethod
    def name():
        return "Upload"

    @staticmethod
    def description():
        return "This function a wrapper for the icgc-storage client"

    def _parser(self, main_parser):
        return

    def _command(self):
        return "icgc-storage-client"