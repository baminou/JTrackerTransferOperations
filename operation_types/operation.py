
import logging
import yaml
from abc import abstractmethod
from jsonschema import Draft4Validator
from operations.documentable import Documentable
import os
import multiprocessing
import threading
import time

class Operation(Documentable):
    """This abstract class is the mother class for operations. An operation is a specific action on a JTracker workflow.
    Two methods have to be implemented for childen classes.
    _schema and _run"""

    def __init__(self, on_running_timer=0.5):
        self.__operation_state = multiprocessing.Manager().dict({'state': 'running'})
        self._on_running_timer = on_running_timer
        self.args = None
        self.output = None
        return

    @property
    def operation_state(self):
        return self.__operation_state

    def set_state(self, state):
        self.__operation_state['state'] = state
        return

    def set_args(self, args):
        self.args = args
        return

    def get_args(self):
        return self.args

    def set_output(self, output):
        self.output = output
        return

    def get_output(self):
        return self.output

    @property
    def on_running_timer(self):
        return self._on_running_timer

    @abstractmethod
    def _schema(self):
        """
        Returns the validation schema for the config file needed to run the operation.
        
        Return:
            dict: A validation dictionary 
        
        Raises:
            NotImplementedError: The method has not been implemented yet
        """
        raise NotImplementedError

    @abstractmethod
    def _run(self):
        """
        The logic of the operation. The config dictionary can be retrieved in the config dictionary: self._config
        
        Raises:
            NotImplementedError: The method has not been implemented yet
        """
        raise NotImplementedError

    @classmethod
    def run(cls, args):
        """
        Main method to run. This method contains the loading+validation of the config file and the _run method
        :param args: 
        :return: 
        """
        obj = cls()
        obj.set_args(args)

        run = obj.before_start()

        if run:
            p1 = multiprocessing.Process(name="main",target=obj._run_wrapper, args=(obj.operation_state, ))
            p2 = multiprocessing.Process(name="timer",target=obj.on_running, args=(obj.operation_state, ))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

            obj.on_completed()

        return

    def _run_wrapper(self, operation_state):
        self.set_output(self._run())
        self.set_state('on_completion')
        return

    @classmethod
    def parser(cls, main_parser):
        obj = cls()
        for parent in obj.__class__.__bases__:
            if issubclass(parent, Operation):
                parent.parser(main_parser)
        obj._parser(main_parser)
        return

    @abstractmethod
    def _parser(self, main_parser):
        return

    @staticmethod
    def environ_or_required(key):
        if os.environ.get(key):
            return {'default': os.environ.get(key)}
        else:
            return {'required': True}

    def before_start(self):
        result = self._before_start()
        self.operation_state['state'] = 'running'
        return result

    def _before_start(self):
        return True

    def on_completed(self):
        self._on_completed()
        self.operation_state['state'] = 'completed'
        return

    def _on_completed(self):
        return

    def on_running(self, d):
        if self.operation_state['state'] == 'running':
            self._on_running()
            threading.Timer(self.on_running_timer, self.on_running,args=[d]).start()
            self.operation_state['state'] = 'running'

    def _on_running(self):
        return
