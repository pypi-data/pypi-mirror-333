# client.py

import json
import requests

from datetime import datetime, timezone

from .config import Config
from .exceptions import LokiConnectionError, LokiSendError

class LokiClient:
    def __init__(self, url, port):
        self.config = Config(url, port)

    def send_log(self, tag, message):
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
            raise LokiConnectionError(f"Failed to connect to Loki server: {e}")
        except requests.exceptions.HTTPError as e:
            raise LokiSendError(f"Failed to send log to Loki: {e}")

        return response.status_code, response.text
