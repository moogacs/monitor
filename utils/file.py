
import yaml
from utils.config import Config

class File:

    @classmethod
    def read_yaml_monitor_file(cls, filepath=None):
        if not filepath:
            filepath = Config.MONITERFILE

        with open(filepath, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as error:
                print(error)

    @classmethod
    def read_time_interval(cls, filepath=None) -> int:

        monitor_file = None
        if not filepath:
            filepath = Config.MONITERFILE

        monitor_file = cls.read_yaml_monitor_file(filepath)
        
        if not monitor_file:
            return 0

        if 'interval' not in monitor_file:
            raise Exception('INTERVAL_NOT_FOUND')
        
        return monitor_file['interval']

    @classmethod
    def read_monitors(cls, filepath=None) -> list:
        monitor_file = None

        if not filepath:
            filepath = Config.MONITERFILE
        
        monitor_file = cls.read_yaml_monitor_file(filepath)
        
        if not monitor_file:
            return []

        if 'monitors' not in monitor_file:
            raise Exception('MONITORS_NOT_FOUND')
        
        return monitor_file['monitors']