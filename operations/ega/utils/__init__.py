
import jsonschema
import requests

def url_exists(url):
    return not requests.get(url).status_code == 404

def project_allowed_on_aws():
    return { 'LIRI-JP', 'PACA-CA' , 'PRAD-CA', 'RECA-EU', 'PAEN-AU', 'PACA-AU',
             'BOCA-UK','OV-AU', 'MELA-AU', 'BRCA-UK', 'PRAD-UK', 'CMDI-UK', 'LINC-JP',
             'ORCA-IN', 'BTCA-SG', 'LAML-KR', 'LICA-FR', 'CLLE-ES', 'ESAD-UK', 'PAEN-IT'}

def yes_or_no(question):
    while 1:
        res = input("%s (Enter y/n)" % (question)).lower()
        if res == "y":
            return True
        if res == "n":
            return False



def ega_job_schema():
    return {
        "properties":{
            'bundle_id' : {'type': 'string'},
            'bundle_type': {'enum': ['run','experiment']},
            "donor_gender": {"enum": ['male','female','unspecified']},
            'ega_analysis_id': {'type':'string'},
            'ega_dataset_id': {"type": "string"},
            "ega_experiment_id": {"type": "string"},
            "ega_metadata_file_name": {"type":"string"},
            "ega_metadata_repo": {"type":"string"},
            "ega_run_id": {"type": "string"},
            "ega_sample_id": {"type": "string"},
            "ega_study_id": {"type": "string"},
            "files": {
                "type": "array",
                "properties": {
                    "ega_file_id": {"type":"string"},
                    "file_md5sum": {"type": "string"},
                    "file_name": {"type":"string"},
                    "size": {"type":"string"}
                }
            },
            "insert_size": {"type":"string"},
            "library_strategy": {"type":"string"},
            "name": {"type":"string"},
            "paired_end": {"type":"string"},
            "project_code": {"type":"string"},
            "reference_genome": {"type":"string"},
            "submitter": {"type":"string"},
            "submitter_donor_id": {"type":"string"},
            "submitter_sample_id": {"type":"string"},
            "submitter_specimen_id": {"type":"string"},
            "submitter_specimen_type": {"type":"string"}
        }
    }

def validate_ega_job_schema(job_json):
    try:
        jsonschema.validate(job_json,ega_job_schema())
    except jsonschema.exceptions.ValidationError as err:
        return str(err.relative_path[0])+"\t"+err.validator+"\t"+str(err.validator_value)