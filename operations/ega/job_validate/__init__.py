
from operation_types.json_operation import JsonOperation
from ..utils import validate_ega_job_schema

class Jobvalidate(JsonOperation):

    @staticmethod
    def name():
        return "Jobvalidate"

    @staticmethod
    def description():
        return "Check if a job json is valid to be run by JTracker"

    def _parser(self, main_parser):
        return

    def _run(self):
        response = validate_ega_job_schema(self.json)
        if not response==None:
            print(self.args.json.name+"\t"+response)
        return True