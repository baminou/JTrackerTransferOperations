
from kernel.operation import Operation
import argparse
import ega_transfer
import csv

class Restage(Operation):

    @staticmethod
    def name():
        return "Restage"

    @staticmethod
    def description():
        return "Create to_stage file from list of EGAFids id"

    def _parser(self, main_parser):
        main_parser.add_argument('--file','-f', dest='list_file',help='File containing list of EGAFIDs to stage', type=argparse.FileType('r'), required=True)
        main_parser.add_argument('-a', '--audit', dest='audit', required=True)
        main_parser.add_argument('-t', '--entity-type', dest='entity_type', required=True, help="This argument only accepts one of two values: run or analysis", choices=['run','analysis'])
        main_parser.add_argument('-o', '--output-file', dest='output_file', required=True)
        return

    def _run(self):
        # Load all EGAFIDs from file
        egafids_to_stage = self.args.list_file.read().splitlines()

        to_stage = ega_transfer.get_files_to_stage(egafids_to_stage, self.args.audit, self.args.entity_type)
        with open(self.args.output_file, 'w') as fp:
            dict_writer = csv.DictWriter(fp, to_stage[0].keys(), delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(to_stage)
