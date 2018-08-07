
from operations.operation import Operation

from ..utils import get_files, update_file
from prompt_toolkit.shortcuts import yes_no_dialog

class Unpublishanalysis(Operation):

    @staticmethod
    def name():
        return "Unpublishanalysis"

    @staticmethod
    def description():
        return "This operation unpublishes an analysis. It changes the md5Sum temporarily and re-save the real md5sum. Make sure that if you are running this function, you" \
               "know what might be the consequences if this operation fails at a critical stage."

    @staticmethod
    def parser(main_parser):
        main_parser.add_argument('server', help="SONG Server URL")
        main_parser.add_argument('study_id', help="Study where the analysis should be unpublished")
        main_parser.add_argument('analysis_id', help="Analysis ID to be unpublished")
        main_parser.add_argument('-t','--token', help="ICGC Access Token", **Operation.environ_or_required('ACCESSTOKEN'))
        main_parser.add_argument('--no-prompt', dest='no_prompt', action='store_false')

        return

    def _run(self, args):
        server = args.server
        study = args.study_id
        analysis = args.analysis_id
        token = args.token

        result = True

        if args.no_prompt:
            result = yes_no_dialog(
                title='Do you want to confirm?',
                text='This operation can make permanent changes to your SONG server in case of failure. Do you still want to continue?')

        if result:
            original_file = get_files(server, study, analysis)[0]
            original_md5 = original_file['fileMd5sum']
            original_file['fileMd5sum'] = "a"*32
            update_file(server, study, original_file['objectId'],token, original_file)
            original_file['fileMd5sum'] = original_md5
            update_file(server, study, original_file['objectId'],token, original_file)
