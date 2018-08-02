
from operations.operation import Operation
from ..utils import is_alive, validate_payload
import json
import argparse

class Validatepayload(Operation):

    @staticmethod
    def name():
        return "sync"

    @staticmethod
    def description():
        return "Synchronize mini-bam file transfer on JTracker with Github Repo"

    @staticmethod
    def parser(main_parser):
        main_parser.add_argument('-c', '--config',
                                         dest='config',
                                         required=True,
                                         help="A valid configuration yaml file",
                                         type=argparse.FileType('r'))

    def _schema(self):
        return {}

    def _run(self,args):
        for error in validate_payload(json.load(args.payload)):
            print(" ls- "+error)
        return