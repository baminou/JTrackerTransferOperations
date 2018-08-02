

import requests
from jsonschema import validate, Draft4Validator
import json


def is_alive(song_server):
    return requests.get('%s/isAlive' % (song_server)).text == "true"

def validate_payload(payload):
    schema = json.loads(requests.get("https://raw.githubusercontent.com/overture-stack/SONG/develop/song-server/src/main/resources/schemas/sequencingRead.json").text)
    v = Draft4Validator(schema)
    errors = []
    for error in sorted(v.iter_errors(payload), key=lambda e: e.path):
        errors.append(error.message)
    return errors

def get_analysis(song_server, study_id, analysis_id):
    return json.loads(requests.get('%s/studies/%s/analysis/%s' % (song_server, study_id, analysis_id)).text)

def get_files(song_server, study_id, analysis_id):
    return json.loads(requests.get('%s/studies/%s/analysis/%s/files' % (song_server, study_id, analysis_id)).text)

def update_file(song_server, study_id, file_id, token, body):
    headers = {'Authorization':'Bearer '+token}
    response = json.loads(requests.put('%s/studies/%s/files/%s' % (song_server, study_id, file_id),json=body,headers=headers).text)
    #print(response)
    return response.get('originalFile')


