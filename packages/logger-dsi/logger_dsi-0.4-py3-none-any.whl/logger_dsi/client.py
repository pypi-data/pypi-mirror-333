# client.py

import json
import requests

from datetime import datetime, timezone

from .config import Config
from .exceptions import LoggerConnectionError, LoggerSendError

class LoggerClient:
    def __init__(self, tag, url, port):
        self.config = Config(tag, url, port)

    def __send_log(self, tag, message):
        # Get the current UTC time and convert to epoch nanoseconds
        now_utc = datetime.now(timezone.utc)
        timestamp_ns = int(now_utc.timestamp() * 1e9)

        # Construct the payload
        data = {
            "streams": [
                {
                    "stream": {
                        "tag": tag
                    },
                    "values": [
                        [str(timestamp_ns), message]
                    ]
                }
            ]
        }

        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.config.get_full_url(), headers=headers, data=json_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise LoggerConnectionError(f"Failed to connect to Logger server: {e}")
        except requests.exceptions.HTTPError as e:
            raise LoggerSendError(f"Failed to send log to Logger: {e}")

        return response.status_code, response.text

    def send_dev_log(self, message):
        return self.__send_log(f"dev_{self.config.get_tag()}", message)
    
    def send_user_log(self, message):
        return self.__send_log(f"user_{self.config.get_tag()}", message)