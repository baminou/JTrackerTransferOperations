
from kernel.operation import Operation

class Dockerfile(Operation):

    @staticmethod
    def name():
        return "Dockerfile"

    @staticmethod
    def description():
        return "Create a docker file at the root of the directory."

    def _parser(self, main_parser):
        return

    def _run(self):
        raise NotImplementedError("Dockerfile not implemented yet.")