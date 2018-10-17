
from . import get_analysis, analysis_is_published, analysis_exists, upload_payload, analysis_is_same_as_json, update_analysis_file, add_to_manifest, get_files, update_file

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

    def unpublish(self, token):
        original_file = get_files(self._song_server, self._study_id, self._analysis_id)[0]
        original_md5 = original_file['fileMd5sum']
        original_file['fileMd5sum'] = "a" * 32
        update_file(self._song_server, self._study_id, original_file['objectId'], token, original_file)
        original_file['fileMd5sum'] = original_md5
        update_file(self._song_server, self._study_id, original_file['objectId'], token, original_file)

    def upload(self, json_payload, access_token):
        return upload_payload(self._song_server,self._study_id, self._analysis_id,json_payload, access_token,ignore_analysis_id_collisions=True)

    def is_same(self, json_payload):
        return analysis_is_same_as_json(self._analysis, json_payload)

    def update_payload(self, json_payload, access_token):
        for i in range(0,len(self._analysis.get('file'))):
            for j in range(0,len(json_payload.get('file'))):
                if self._analysis.get('file')[i].get('fileName') == json_payload.get('file')[j].get('fileName'):
                    update_analysis_file(self._song_server,self._study_id,self._analysis.get('file')[i].get('objectId'),json_payload.get('file')[j],access_token)
        return

    def create_manifest(self, json_payload, outfile):
        for i in range(0, len(json_payload.get('file'))):
            add_to_manifest(self._song_server, self._study_id, self._analysis_id, json_payload.get('file')[i].get('fileName'),json_payload.get('file')[i].get('fileMd5sum'),outfile)
        return

    def convert_manifest_to_json(self, manifest):
        with open(manifest, 'r') as f:
            manifest_json = {}
            manifest_json['analysis_id'] = f.readline().split('\t')[0]
            manifest_json['files'] = []
            for line in f.readlines():
                _file = {}
                _file['object_id'] = line.split('\t')[0]
                _file['file_name'] = line.split('\t')[1]
                _file['md5'] = line.split('\t')[2].strip('\n')
                manifest_json['files'].append(_file)
            return manifest_json

