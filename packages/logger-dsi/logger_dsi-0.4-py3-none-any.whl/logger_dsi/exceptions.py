# exceptions.py

class LoggerClientException(Exception):
    """Base exception for LoggerClient errors."""
    pass

class LoggerConnectionError(LoggerClientException):
    """Exception raised for errors in the connection."""
    pass

class LoggerSendError(LoggerClientException):
    """Exception raised for errors while sending logs."""
    pass
