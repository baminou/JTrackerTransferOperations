
from operation_types.operation import Operation

from ..utils import get_files, update_file
from ..utils.SongAnalysis import SongAnalysis
from prompt_toolkit.shortcuts import yes_no_dialog

class Unpublishanalysis(Operation):

    @staticmethod
    def name():
        return "Unpublishanalysis"

    @staticmethod
    def description():
        return "This operation unpublishes an analysis. It changes the md5Sum temporarily and re-save the real md5sum. Make sure that if you are running this function, you" \
               "know what might be the consequences if this operation fails at a critical stage."

    def _parser(self, main_parser):
        main_parser.add_argument('server', help="SONG Server URL")
        main_parser.add_argument('study_id', help="Study where the analysis should be unpublished")
        main_parser.add_argument('analysis_id', help="Analysis ID to be unpublished")
        main_parser.add_argument('-t','--token', help="ICGC Access Token", **Operation.environ_or_required('ACCESSTOKEN'))
        main_parser.add_argument('--no-prompt', dest='no_prompt', action='store_false')

        return

    def _run(self):

        result = True

        #if self.args.no_prompt:
        #    result = yes_no_dialog(
        #        title='Do you want to confirm?',
        #        text='This operation can make permanent changes to your SONG server in case of failure. Do you still want to continue?')

        if result:
            analysis = SongAnalysis(self.args.server, self.args.study_id, self.args.analysis_id)
            analysis.unpublish(self.args.token)
