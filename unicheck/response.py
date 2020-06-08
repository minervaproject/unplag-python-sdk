"""
This module represents responce abstraction and exceptions.
"""

from requests.models import Response


class UnplagMainException(Exception):
    """
    Class representing general wide exception in Unplag Python API
    """
    pass


class UnplagHTTPException(UnplagMainException):
    """
    Class using for raising exceptions in format:
        "status_code status_info responce"
    """

    status_codes = {
        200: 'OK',
        400: 'Invalid params or unsupported content type',
        401: 'Unauthorized',
        402: 'Insufficient funds to start check',
        403: 'Forbidden. Do not have access to entity',
        404: 'Entity not found',
        405: 'Invalid method',
        406: '"fmt" param or "Accept" header are not supported',
        413: 'File is too big or contains than 100k words',
        415: 'Unsupported file format or file is corrupted',
        429: 'Too many requests',
        500: 'Internal server error',
        503: 'Maintenance'
    }

    def __init__(self, status_code, response=None):
        self.status_code = status_code
        self.response = response
        self.resp = self.status_codes[status_code]

    def __str__(self):
        return repr('%s %s %s' % (self.status_code, self.resp, self.response))


class UnplagResponse(object):
    """
    Creating general response object.
    It validates if response is valid, than parse additional info,
    loads json from responce, check for status codes, etc.
    """

    def __init__(self, response):

        if not isinstance(response, Response):
            raise UnplagMainException('Object is not a valid response!')

        self.full_response_obj = response
        self.url = response.url
        self.status_code = response.status_code
        self.headers = response.headers
        self.text = response.text
        self.response = response.json()

    def check_responce(self):
        """
        Check if response is valid
        :rtype: object
        :return: boolean
        """
        if self.status_code != 200 and self.status_code in UnplagHTTPException.status_codes.keys():
            raise UnplagHTTPException(self.status_code, self.text)

        if not self.response['result']:
            raise UnplagHTTPException(self.status_code, self.text)

        return True

    def __str__(self):
        return repr(self.text)


class UnplagFileResponse(UnplagResponse):
    """
    Representing response object for File methods
    """
    def __init__(self, response):
        UnplagResponse.__init__(self, response)

        self.check_responce()


class UnplagCheckResponse(UnplagResponse):
    """
    Representing response object for Check methods
    """
    def __init__(self, response):
        UnplagResponse.__init__(self, response)

        self.check_responce()


class UnplagDirectoryResponse(UnplagResponse):
    """
    Representing response object for Check methods
    """
    def __init__(self, response):
        UnplagResponse.__init__(self, response)

        self.check_responce()
