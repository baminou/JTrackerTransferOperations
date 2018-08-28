
from operation_types.operation import Operation
import csv
import argparse
import ast
import ega_transfer
from termcolor import colored


class Tostagestatus(Operation):

    @staticmethod
    def name():
        return "Tostagestatus"

    @staticmethod
    def description():
        return "Show the status of the files that have to be staged on EGA server"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='to_stage_tsv', type=argparse.FileType('r'))
        main_parser.add_argument(dest='aspera_server')
        main_parser.add_argument(dest='aspera_user')
        return

    def _run(self):
        reader = csv.DictReader(self.args.to_stage_tsv, delimiter='\t')
        ega_box_fids = ega_transfer.get_ega_box_fids(self.args.aspera_server,self.args.aspera_user)

        for row in reader:
            file_size = row.get('file_size')
            study = row.get('project_code')
            egafid = row.get('ega_file_id')
            missed_cpt = 0
            state = None
            col = None
            if egafid in ega_box_fids:
                state = "staged"
                col = "green"
            else:
                state = "unstaged"
                col = "red"
                missed_cpt = missed_cpt + 1

            print(egafid+"\t"+file_size+"\t"+"\t"+study+"\t"+colored(state, col))
        print("### "+str(missed_cpt)+" EGAFIDs are not staged")

