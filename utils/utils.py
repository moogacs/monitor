
import re
from utils.config import Config

class Utils:
    
    @classmethod
    def is_valid_URL(cls, url: str) -> bool:
        return  bool(re.match(Config.URL_REGEX, url))