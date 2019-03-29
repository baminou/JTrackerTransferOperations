
import requests

def get_analysis(song_url, study, analysis_id):
    return requests.get('%s/studies/%s/analysis/%s' % (song_url,study,analysis_id)).json()