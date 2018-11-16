
from kernel.library import Library
from .list_queues import Listqueues

class jtracker(Library):

    @staticmethod
    def name():
        return "jtracker"

    @staticmethod
    def description():
        return "Not description provided"

    @staticmethod
    def operations():
        return {
            'list:queues': Listqueues
        }