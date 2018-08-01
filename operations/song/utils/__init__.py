

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
