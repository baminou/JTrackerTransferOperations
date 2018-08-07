import logging
import yaml
from abc import ABC, abstractmethod
from jsonschema import Draft4Validator
from .documentable import Documentable
import os
from .operation import Operation


class ConfigOperation(Operation):

    def _validate_json_config(self, json):
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

    def load_config(self, yml_file_p):
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

    def _parser(self, main_parser):
        main_parser.add_argument('config')
        return main_parser