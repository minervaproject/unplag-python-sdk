"""
This module implements a friendly interface between the Unicheck and client.
Full API documentation can be found at:
https://unicheck.com/api/doc
"""

from .connection import Connection
from .file import File
from .directory import Directory
from .check import Check


class Unicheck(object):
    """ User interface to Unicheck """

    def __init__(self, key, secret, server='https://unicheck.com'):
        """
        Construct a Unicheck client instance
        :arg server: Unicheck endpoint, should be a string and contains valid url,
            default is  'https://unicheck.com'

        :arg key: must be a string, from valid API key
            from https://unicheck.com/profile/apisettings

        :arg secret: must be a string, from valid API secret
            from https://unicheck.com/profile/apisettings
        """

        # Rip off trailing slash since all urls depend on that
        if server.endswith('/'):
            self.server = server[:-1]
        else:
            self.server = server

        self.key = key
        self.secret = secret

        # Create connection and session
        conn = Connection(self.key, self.secret, self.server)
        conn.create()
        self.oauth_session = conn.oauth_session

        # Initialize File entity
        self.file = File(self.oauth_session, self.server)

        # Initialize Directory entity
        self.directory = Directory(self.oauth_session, self.server)

        # Initialize Check entity
        self.check = Check(self.oauth_session, self.server)
