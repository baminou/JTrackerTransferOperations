
from operation_types.yml_config_operation import YmlConfigOperation
import csv

class Report(YmlConfigOperation):

    @staticmethod
    def name():
        return "Report"

    @staticmethod
    def description():
        return "Create a visual report of the EGA transfer"

    def _config_schema(self):
        return {
            "tsvs": {
                "type": "array"
            },
            "required": ['tsvs']
        }

    def _parser(self, main_parser):
        return

    def _run(self):
        files = dict()
        for tsv in self.config.get('tsvs'):
            with open(tsv,'r') as fp:
                reader = csv.DictReader(fp, delimiter='\t')
                for row in reader:
                    egafid = row.get('EGA File Accession')
                    study = row.get('ICGC DCC Project Code')
                    files[egafid] = {'study':study}
        print(files)