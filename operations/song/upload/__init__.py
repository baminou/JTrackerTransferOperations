
from operation_types.json_operation import JsonOperation
import os
from ..utils import payload_schema, get_analysis, analysis_exists
from ..utils.SongAnalysis import SongAnalysis

class Upload(JsonOperation):

    @staticmethod
    def name():
        return "Upload"

    @staticmethod
    def description():
        return "Upload Song payload"

    def _config_schema(self):
        return payload_schema()

    def _parser(self, main_parser):
        main_parser.add_argument('study_id', help="Study ID")
        main_parser.add_argument('song_server', help="Server URL")
        #main_parser.add_argument('--force', dest='force',help="Force the song upload no matter what.", action='store_false')
        #main_parser.add_argument('-o', '--output', dest="output", help="Output manifest file", required=True)
        main_parser.add_argument('-t', '--access-token', dest="access_token", default=os.environ.get('ACCESSTOKEN', None),help="Server URL")
        return

    def _run(self):
        song_server = self.args.song_server
        study_id = self.args.study_id
        analysis_id = self.json.get('analysisId')

        song_analysis = SongAnalysis(song_server, study_id, analysis_id)

        # If the payload has already been uploaded
        if song_analysis.exists_on_server():

            #If the payload is already published
            if song_analysis.is_published():
                raise Exception("The song analysis %s has already been published." % (analysis_id))
            else:
                print(song_analysis.is_same(self.json))

        else:
            song_analysis.upload(json_payload=self.json, access_token=self.args.access_token)

        return