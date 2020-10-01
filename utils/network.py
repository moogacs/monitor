import re
import requests
from utils.config import Config
from utils.utils import Utils

class Network:

    @classmethod
    def get_website_status(cls, task):
        pattern = None
        name = None
        has_pattern = None

        if 'pattern' in task:
            pattern = task['pattern']
            has_pattern = False

        if 'name' in task:
            name = task['name']

        # if url is not existsed shoudl return 
        if 'url' not in task:
            print("CORRUPTED_URL_VALUE_ERROR with item => " + str(task))
            return None

        # if url is not valid should return
        if not Utils.is_valid_URL(task['url']):
            print("PARSE_URL_ERROR", task['url'])
            return None

        url = task['url']
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            response_time = str(round(response.elapsed.total_seconds(),2))
            status_code = response.status_code
            reason = response.reason
            
            if pattern:
                has_pattern = bool(re.search(pattern, response.text))
            
        except requests.exceptions.ConnectionError:
            status_code = "503"
            reason = 'ConnectionError'
            response_time = 0
        except requests.exceptions.HTTPError:
            status_code = "000"
            reason = 'HTTPError'
            response_time = 0
            
        website_status = {
            "name": name,
            "url": url,
            "status_code":  status_code,
            "reason": reason,
            "response_time": response_time,
            "pattern": pattern,
            "has_pattern": has_pattern
        }
    
        return website_status