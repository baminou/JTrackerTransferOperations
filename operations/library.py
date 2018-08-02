
from .documentable import Documentable
import tableprint as tp
import inspect
from termcolor import colored
from tabulate import tabulate


class Library(Documentable):

    @staticmethod
    def operations():
        return {}
