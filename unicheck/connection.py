"""
This module builds connection to Unplag from client.
"""

from requests_oauthlib import OAuth1Session


class Connection(object):
    """ Representation of connection abstact in Unplag
        Not needed to change something here. """

    def __init__(self, key, secret, server):
        self.key = key
        self.secret = secret
        self.server = server
        self.oauth_session = None

    def create(self):
        """
        Create connection using Oauth 1.0

        :return: oauth object for connection
        """

        self.oauth_session = OAuth1Session(client_key=self.key, client_secret=self.secret)

    def ping(self):
        """
        Check connection and authenticating using Oauth 1.0
        If ok, return True

        :return: boolean
        """

        self.create()

        resp = self.oauth_session.get(self.server + '/api/v2/file/get')
        if resp.status_code == 401:
            raise Exception('Unauthorized')
        else:
            return True
