
import abc

class JTracker:

    def __init__(self):
        return

    @abc.abstractmethod
    def get_job_ids(self, state=None):
        raise NotImplementedError

    @abc.abstractmethod
    def get_job_data(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_job(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_jobs(self, state=None):
        raise NotImplementedError