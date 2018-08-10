
from operation_types.json_operation import JsonOperation
import requests

class Uploadsongpayload(JsonOperation):

    @staticmethod
    def name():
        return "upload_song_payload"

    @staticmethod
    def description():
        return "Uploadsongpayload has not been documented yet."

    def _parser(self, main_parser):
        main_parser.add_argument('song_server')
        return

    def _run(self):
        payload = self.json
        analysis_id = payload.get('analysisId')
        study = payload.get('study')
        print(self.analysis_is_published(self.args.song_server,study,analysis_id))
        return True

    def analysis_exists(self, song_server, study_id, analysis_id):
        response = requests.get('%s/studies/%s/analysis/%s' % (song_server, study_id, analysis_id))
        return response.status_code == 200

    def analysis_is_published(self, song_server, study_id, analysis_id):
        response = requests.get('%s/studies/%s/analysis/%s' % (song_server, study_id, analysis_id)).json()
        return response.get('analysisState') == "PUBLISHED"

    def analysis_save(self, song_server, study_id, payload_json, token):
        response = requests.post('%s/upload/%s' % (song_server, study_id),{'json_payload':payload_json},headers={'Authorization':'Bearer %s' % token})
        return response.status_code