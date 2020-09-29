import re
import requests
from utils.config import Config

class Network:

    def get_website_status(name, url, pattern):
            has_pattern = False
            
            if not bool(re.match(Config.URL_REGEX, url)):
                print("PARSE_URL_ERROR", url)
                return None

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
                
            return {
                "name": name,
                "website": url,
                "status_code":  status_code,
                "reason": reason,
                "response_time": response_time,
                "pattern": pattern,
                "has_pattern": has_pattern
            }