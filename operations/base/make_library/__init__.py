
from operations.operation import Operation

from ..utils import library_create

class Makelibrary(Operation):
    def _schema(self):
        return {}

    def _run(self,args):
        library_create(args.name)
        return