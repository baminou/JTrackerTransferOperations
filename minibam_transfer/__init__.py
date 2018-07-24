
import requests
import json

def get_jobnames_state(host, user, queues=[]):
    jobs = {}
    for queue in queues:
        for job in json.loads(requests.get("%s/api/jt-jess/v0.1/jobs/owner/%s/queue/%s" % (host, user,queue)).text):
            jobs[job.get('name')] = job.get('state')
    return jobs