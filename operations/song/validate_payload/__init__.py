
from operations.operation import Operation
from prompt_toolkit.shortcuts import yes_no_dialog
from ..utils import is_alive, validate_payload
import json

class Validatepayload(Operation):
    def _schema(self):
        return {}

    def _run(self,args):
        for error in validate_payload(json.load(args.payload)):
            print(" ls- "+error)
        return