
import logging
import yaml
from abc import ABC, abstractmethod
from jsonschema import Draft4Validator
from .documentable import Documentable
import os
import multiprocessing
import threading
import time

class Operation(Documentable):
    """This abstract class is the mother class for operations. An operation is a specific action on a JTracker workflow.
    Two methods have to be implemented for childen classes.
    _schema and _run"""

    def __init__(self, on_running_timer=0.5):
        self._operation_state = multiprocessing.Manager().dict({'state': 'running'})
        self._on_running_timer = on_running_timer
        return

    @property
    def operation_state(self):
        return self._operation_state

    def set_state(self, state):
        self._operation_state['state'] = state
        return

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
    def _run(self, args):
        """
        The logic of the operation. The config dictionary can be retrieved in the config dictionary: self._config
        
        Args:
            args: The command line arguments needed to run the operation
        
        Raises:
            NotImplementedError: The method has not been implemented yet
        """
        raise NotImplementedError

    def _validate_json_config(self,json):
        """
        Validate a dictionary against the _schema method.
        
        Args:
            json: A valid dictionary
        """
        logging.debug("Validating config data")
        v = Draft4Validator(self._schema())
        errors = sorted(v.iter_errors(json), key=lambda e: e.path)
        if len(errors) > 0:
            for error in errors:
                logging.error(error.message)
            exit(1)
        logging.debug("Config data validated")
        return

    def load_config(self,yml_file_p):
        """
        Transform an opened yaml file in json
        
        Args:
            yml_file_p:  A pointer to a file opened in read mode
        
        Return:
            dict: The yaml file in dict format
        """
        logging.debug("Loading config file")
        response = yaml.load(yml_file_p)
        logging.debug("Config file loaded")
        return response

    @classmethod
    def run(cls, args):
        """
        Main method to run. This method contains the loading+validation of the config file and the _run method
        :param args: 
        :return: 
        """
        # Load the config file containing the needed information
        # If the config file has something missing, a validation error might raise, depending on the error
        #if hasattr(args,'config'):
        #    logging.info("Configuration yaml file")
        #    self._config = self.load_config(args.config)
        #    self._validate_json_config(self._config)
        operation = cls()
        #operation._run(args)
        #return

        obj = cls()

        obj.before_start()

        p1 = multiprocessing.Process(name="main",target=obj._run_wrapper, args=(args, obj.operation_state, ))
        p2 = multiprocessing.Process(name="timer",target=obj.on_running, args=(obj.operation_state, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        obj.on_completed()

        return

    def _run_wrapper(self, args, operation_state):
        self._run(args=args)
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

    def _parser(self, main_parser):
        return main_parser

    @staticmethod
    def environ_or_required(key):
        if os.environ.get(key):
            return {'default': os.environ.get(key)}
        else:
            return {'required': True}

    def before_start(self):
        self._before_start()
        self.operation_state['state'] = 'running'
        return

    def _before_start(self):
        return

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
