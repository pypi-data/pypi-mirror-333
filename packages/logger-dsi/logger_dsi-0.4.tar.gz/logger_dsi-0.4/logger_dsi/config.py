# config.py

class Config:
    def __init__(self, tag, url, port):
        self.tag = tag
        self.url = url
        self.port = port
        
    def get_tag(self):
        return self.tag

    def get_full_url(self):
        return f"http://{self.url}:{self.port}/loki/api/v1/push"
