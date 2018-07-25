
import logging

from entities.ega_audit import EGAAudit
import json
import ega_transfer
import os
from operations.operation import Operation
from entities.ega import EGA

class EGADbox(Operation):
    def _run(self,args):
        ega = EGA(args.aspera_server, args.aspera_user)
        for file in ega.dbox():
            print(file)