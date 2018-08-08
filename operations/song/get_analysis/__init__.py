
from operation_types.operation import Operation
from ..utils import get_analysis
import json

class Getanalysis(Operation):

    @staticmethod
    def name():
        return "Getanalysis"

    @staticmethod
    def description():
        return "Getanalysis has not been documented yet."

    def _parser(self, main_parser):
        main_parser.add_argument('song_server_url', help="URL of the song server")
        main_parser.add_argument('study_id', help="Study ID of the analysis")
        main_parser.add_argument('analysis_id', help="Analysis id to retrieve")
        return

    def _run(self):
        print(json.dumps(get_analysis(self.args.song_server_url, self.args.study_id, self.args.analysis_id)))
        return True