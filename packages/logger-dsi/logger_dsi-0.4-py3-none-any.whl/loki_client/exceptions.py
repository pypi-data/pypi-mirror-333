# exceptions.py

class LokiClientException(Exception):
    """Base exception for LokiClient errors."""
    pass

class LokiConnectionError(LokiClientException):
    """Exception raised for errors in the connection."""
    pass

class LokiSendError(LokiClientException):
    """Exception raised for errors while sending logs."""
    pass
