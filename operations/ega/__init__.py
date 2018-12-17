

from kernel.library import Library
from .job import Job
from .dbox import Dbox
from .to_stage import ToStage
from .to_delete import ToDelete
from .runnable import Runnable
from .is_alive import Isalive
from .sync_files import SyncFiles
from .to_stage_status import Tostagestatus
from .report import Report
from .old_fids import Oldfids
from .new_fids import Newfids
from .job_validate import Jobvalidate
from .publish_state import Publishstate
from .publish_states import Publishstates

class EGA(Library):

    @staticmethod
    def name():
        return "ega"

    @staticmethod
    def description():
        return "EGA Transfer to collaboratory operations"

    @staticmethod
    def parser(main_parser):
        return

    @staticmethod
    def operations():
        return {
            'job': Job,
            'dbox': Dbox,
            'to_stage': ToStage,
            'to_delete': ToDelete,
            'runnable': Runnable,
            'is_alive': Isalive,
            'sync': SyncFiles,
            'to_stage:status': Tostagestatus,
            'report': Report,
            'old:fids': Oldfids,
            'new:fids': Newfids,
            'job:validate': Jobvalidate,
            'publish:state': Publishstate,
            'publish:states': Publishstates
        }
