
import yaml
from utils.config import Config

class File:
    def read_yaml_monitor_file(filepath=None):
        if not filepath:
            filepath = Config.MONITERFILE

        with open(filepath, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as error:
                print(error)


    def read_time_interval(filepath=None) -> int:
        monitor_file = None

        if not filepath:
            filepath = Config.MONITERFILE

        with open(filepath, 'r') as stream:
            try:
                monitor_file = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                print(error)
        
        if not monitor_file:
            return 0

        if 'interval' not in monitor_file:
            raise Exception('INTERVAL_NOT_FOUND')
            return 0
        
        return monitor_file['interval']