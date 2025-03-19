import copy
import json
import os

import yaml

from google.protobuf import json_format

from traceableai.config import config_pb2
from traceableai.config.default import DEFAULT
from traceableai.config.environment import overwrite_with_environment
from traceableai.custom_logger import get_custom_logger
logger = get_custom_logger(__name__)

REMOTE_CONFIG_KEY = 'remote_config'
BLOCKING_CONFIG_KEY = 'blocking_config'

class Config(): # pylint:disable=R0903
    _instance = None

    def __new__(cls):
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.config = build_config()


# We don't want to update a value that is set with an unset value
def merge_config(base_config, overriding_config):
    for key in overriding_config:
        if key in base_config and isinstance(base_config[key], dict):
            if key in overriding_config:
                base_config[key] = merge_config(base_config[key], overriding_config[key])
        else:
            base_config[key] = overriding_config[key]
    return base_config
# Config load ordering
# 1.) Use the defaults
# 2.) Override the defaults with config file
# 3.) Override the config file with env vars
def build_config():
    traceable_config = config_pb2.AgentConfig()
    config_dict = copy.deepcopy(DEFAULT)
    file_dict = read_from_file()
    if file_dict is not None:
        merge_config(config_dict, file_dict)

    json_string = json.dumps(config_dict)
    logger.debug(json_string)
    json_format.Parse(json_string, traceable_config, ignore_unknown_fields=True)

    overwrite_with_environment(traceable_config)

    return traceable_config

def read_from_file():
    config_path = _config_file_path()
    if config_path is None or not os.path.exists(config_path):
        logger.debug("TA_CONFIG_FILE path not set")
        return None

    with open(config_path, 'r', encoding="UTF-8") as config_file:
        try:
            file_dict =  yaml.safe_load(config_file)
            # setting the new remote config with deprecated one if the new one doesn't exist
            if REMOTE_CONFIG_KEY not in file_dict and BLOCKING_CONFIG_KEY in file_dict and \
                    REMOTE_CONFIG_KEY in file_dict[BLOCKING_CONFIG_KEY]:
                file_dict[REMOTE_CONFIG_KEY] = file_dict[BLOCKING_CONFIG_KEY][REMOTE_CONFIG_KEY]
                del file_dict[BLOCKING_CONFIG_KEY][REMOTE_CONFIG_KEY]

            return file_dict
        except yaml.YAMLError as exc:
            logger.debug(exc)
            return None

def _config_file_path():
    config_path = os.environ.get('TA_CONFIG_FILE', None)
    if config_path is None:
        return None
    return config_path
