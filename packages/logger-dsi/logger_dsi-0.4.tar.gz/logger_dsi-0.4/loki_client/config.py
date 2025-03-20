# config.py

class Config:
    def __init__(self, url, port):
        self.url = url
        self.port = port

    def get_full_url(self):
        return f"http://{self.url}:{self.port}/loki/api/v1/push"
