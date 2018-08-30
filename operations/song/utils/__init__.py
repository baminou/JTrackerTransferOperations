

import requests
from jsonschema import validate, Draft4Validator
import json
from deepdiff import DeepDiff, DeepSearch
import operator


def is_alive(song_server):
    return requests.get('%s/isAlive' % (song_server)).text == "true"

def payload_schema():
    return json.loads(requests.get("https://raw.githubusercontent.com/overture-stack/SONG/develop/song-server/src/main/resources/schemas/sequencingRead.json").text)

def validate_payload(payload):
    schema = payload_schema()
    v = Draft4Validator(schema)
    errors = []
    for error in sorted(v.iter_errors(payload), key=lambda e: e.path):
        errors.append(error.message)
    return errors

def get_analysis(song_server, study_id, analysis_id):
    response = requests.get('%s/studies/%s/analysis/%s' % (song_server, study_id, analysis_id))
    if response.status_code == 404:
        raise Exception("Analysis %s/%s does not exist on the song server %s." % (study_id, analysis_id, song_server))
    return json.loads(response.text)

def analysis_exists(song_server, study_id, analysis_id):
    response = requests.get('%s/studies/%s/analysis/%s' % (song_server, study_id, analysis_id))
    if response.status_code == 404:
        return False
    return True

def analysis_is_published(song_server, study_id, analysis_id):
    if not analysis_exists(song_server, study_id, analysis_id):
        raise Exception("Analysis %s/%s does not exist on the song server %s." % (study_id, analysis_id, song_server))

    analysis = get_analysis(song_server, study_id, analysis_id)
    return analysis.get('analysisState') == 'PUBLISHED'

def get_files(song_server, study_id, analysis_id):
    return json.loads(requests.get('%s/studies/%s/analysis/%s/files' % (song_server, study_id, analysis_id)).text)

def update_file(song_server, study_id, file_id, token, body):
    headers = {'Authorization':'Bearer '+token}
    response = json.loads(requests.put('%s/studies/%s/files/%s' % (song_server, study_id, file_id),json=body,headers=headers).text)
    #print(response)
    return response.get('originalFile')

def suppress_analysis(song_server, study_id, analysis_id, token):
    if analysis_is_published(song_server, study_id, analysis_id):
        raise Exception("You cannot supress a PUBLISHED analysis. Make it unpublished first.")
    headers = {'Authorization':'Bearer '+token}
    response = requests.put('%s/studies/%s/analysis/suppress/%s' % (song_server, study_id, analysis_id),headers=headers)
    if not response.status_code == 200:
        raise Exception("The analysis %s could not be supressed." % (analysis_id))

def upload_payload(song_server, study_id, analysis_id, payload,token, ignore_analysis_id_collisions=False):
    if analysis_exists(song_server,study_id, analysis_id):
        raise Exception("The payload %s/%s already exists" % (study_id, analysis_id))

    headers = {'Authorization':'Bearer '+token}
    response = json.loads(requests.post('%s/upload/%s' % (song_server, study_id), json=payload, headers=headers).text)
    upload_id = response.get('uploadId')
    upload_response = json.loads(requests.get('%s/upload/%s/status/%s' % (song_server, study_id, upload_id)).text)

    if not upload_response.get('state') == "VALIDATED":
        raise Exception('The song payload could not be uploaded, reason: %s' % (response.get('errors')[0]))

    save_response = requests.post('%s/upload/%s/save/%s' % (song_server, study_id, upload_id), data={'ignoreAnalysisIdCollisions':ignore_analysis_id_collisions} ,headers=headers)
    if not save_response.status_code == 200:
        raise Exception("The payload %s/%s could not be uploaded." % (study_id, analysis_id))

def analysis_is_same_as_json(analysis, payload):
    del analysis['analysisState']
    del analysis['experiment']['info']

    for i in range(0, len(analysis.get('sample'))):
        del analysis.get('sample')[0]['info']
        del analysis.get('sample')[0]['specimen']['info']
        del analysis.get('sample')[0]['donor']['info']

    for i in range(0,len(analysis.get('file'))):
        del analysis.get('file')[i]['info']
        del analysis.get('file')[i]['studyId']
        del analysis.get('file')[i]['analysisId']
        del analysis.get('file')[i]['objectId']
    return DeepDiff(analysis.get('file'),payload.get('file'), ignore_order=True) == {}

