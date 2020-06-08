"""
This module implements a friendly interface between the Unplag and client.
Full API documentation can be found at:
https://unplag.com/api/doc
"""

from .connection import Connection
from .file import File
from .directory import Directory
from .check import Check


class Unplag(object):
    """ User interface to Unplag """

    def __init__(self, key, secret, server='https://unplag.com'):
        """
        Construct a Unplag client instance
        :arg server: Unplag endpoint, should be a string and contains valid url,
            default is  'https://unplag.com'

        :arg key: must be a string, from valid API key
            from https://unplag.com/profile/apisettings

        :arg secret: must be a string, from valid API secret
            from https://unplag.com/profile/apisettings
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