
import logging
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError

class Operation:

    def __init__(self):
        self._config = {}

    def _schema(self):
        raise NotImplementedError

    def _validate_json_config(self,json):
        logging.debug("Validating config data")
        try:
            validate(json, self._schema())
        except ValidationError as err:
            logging.error(str(err.message))
            exit(1)
        logging.debug("Config data validated")
        return

    def load_config(self,yml_file):
        logging.debug("Loading config file: " + yml_file)
        with open(yml_file,'r') as stream:
            response = yaml.load(stream)
        logging.debug("Config file loaded: " + yml_file)
        return response

    def run(self, args):
        # Load the config file containing the needed information
        # If the config file has something missing, a validation error might raise, depending on the error
        logging.info("Configuration yaml file")
        self._config = self.load_config(args.config)
        self._validate_json_config(self._config)
        self._run(args)

    def _run(self, args):
        raise NotImplementedError