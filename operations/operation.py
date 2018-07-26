
import logging
import yaml
from abc import ABC, abstractmethod
from jsonschema import Draft4Validator

class Operation:
    """This abstract class is the mother class for operations. An operation is a specific action on a JTracker workflow.
    Two methods have to be implemented for childen classes.
    _schema and _run"""

    def __init__(self,config={}):
        self._config = config

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

    def run(self, args):
        """
        Main method to run. This method contains the loading+validation of the config file and the _run method
        :param args: 
        :return: 
        """
        # Load the config file containing the needed information
        # If the config file has something missing, a validation error might raise, depending on the error
        if hasattr(args,'config'):
            logging.info("Configuration yaml file")
            self._config = self.load_config(args.config)
            self._validate_json_config(self._config)
        self._run(args)