
from operations.operation import Operation

class NewOperation(Operation):
    def _schema(self):
        return {}

    def _run(self,args):
        return