import json
from werkzeug.exceptions import HTTPException

from flask import Response

class HTTPExceptionFactory(HTTPException):
    @staticmethod
    def get_HTPP_Exception(description, code):
        exception = HTTPExceptionFactory(description, code)
        return exception

    def __init__(self, description, code):
        self.description = description
        self.code = code
        self.response = Response()


