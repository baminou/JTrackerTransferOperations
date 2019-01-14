
import ega_transfer
import csv
from kernel.operation import Operation
import sys

class Tostagelist(Operation):

    @staticmethod
    def name():
        return "Tostagelist"

    @staticmethod
    def description():
        return "Create a list to stage from egafids"

    def _parser(self, main_parser):
        main_parser.add_argument('-a', '--audit', dest='audit', required=True)
        main_parser.add_argument('-t', '--entity-type', dest='entity_type', required=True, help="This argument only accepts one of two values: run or analysis", choices=['run','analysis'])
        main_parser.add_argument('-f', '--egafids', dest='egafids', nargs='+',required=True)

    def _run(self):
        to_stage = ega_transfer.get_files_to_stage(list(set(self.args.egafids)), self.args.audit, self.args.entity_type)
        dict_writer = csv.DictWriter(sys.stdout, to_stage[0].keys(), delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(to_stage)