
from operation_types.json_operation import JsonOperation
import os
from ..utils import payload_schema, get_analysis, analysis_exists
from ..utils.SongAnalysis import SongAnalysis
from argparse import FileType
import json

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
        main_parser.add_argument("output", help="Output manifest file")
        main_parser.add_argument('-j','--json',dest="output_json", help="Output manifest file", required=False)
        main_parser.add_argument('-t', '--access-token', dest="access_token", default=os.environ.get('ACCESSTOKEN', None),help="Server URL")
        return

    def _run(self):
        song_server = self.args.song_server
        study_id = self.args.study_id
        analysis_id = self.json.get('analysisId')

        song_analysis = SongAnalysis(song_server, study_id, analysis_id)

        # If the payload has already been uploaded
        if song_analysis.exists_on_server():

            #If the payload is already published, the program stops
            if song_analysis.is_published():
                raise Exception("The song analysis %s has already been published." % (analysis_id))
            else:
                if not song_analysis.is_same(self.json):
                    #Upload the new song payload
                    song_analysis.update_payload(self.json,self.args.access_token)
        else:
            song_analysis.upload(json_payload=self.json, access_token=self.args.access_token)

        with open(self.args.output, 'w') as fp:
            song_analysis.create_manifest(json_payload=self.json,outfile=fp)

        if not self.args.output_json == None:
            with open(self.args.output_json, 'w') as fp:
                json.dump(song_analysis.convert_manifest_to_json(self.args.output),fp)

        return