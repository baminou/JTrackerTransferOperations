
from . import get_analysis, analysis_is_published, analysis_exists, upload_payload, analysis_is_same_as_json

class SongAnalysis(object):
    def __init__(self, song_server, study_id, analysis_id):
        self._song_server = song_server
        self._study_id = study_id
        self._analysis_id = analysis_id
        self._analysis = None
        if analysis_exists(song_server, study_id, analysis_id):
            self._analysis = get_analysis(song_server, study_id, analysis_id)
        return

    def exists_on_server(self):
        return not self._analysis == None

    def is_published(self):
        return analysis_is_published(self._song_server,self._study_id, self._analysis_id)

    def is_unpublished(self):
        return not self.is_published()

    def upload(self, json_payload, access_token):
        return upload_payload(self._song_server,self._study_id, self._analysis_id,json_payload, access_token,ignore_analysis_id_collisions=True)

    def is_same(self, json_payload):
        return analysis_is_same_as_json(self._analysis, json_payload)

