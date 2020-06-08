import unittest
from requests_oauthlib import OAuth1Session

from unicheck import Unicheck
from unicheck.connection import Connection
from unicheck.check import Check
from unicheck.file import File


#   Initialize empty Unicheck entity
un = Unicheck('test_key', 'test_secret', server='http://unicheck.com/')


class TestUnicheckEntity(unittest.TestCase):
    def test_unicheck_auth(self):
        self.assertEqual(un.server, 'http://unicheck.com')
        self.assertEqual(un.key, 'test_key')
        self.assertEqual(un.secret, 'test_secret')


class TestConnectionEntity(unittest.TestCase):
    def test_connection(self):
        conn = Connection('test_key', 'test_secret', 'http://unicheck.com')
        conn.create()

        self.assertIsNotNone(conn.oauth_session)
        self.assertIsInstance(conn.oauth_session, OAuth1Session)
        self.assertEqual(type(conn.oauth_session), type(un.oauth_session))
        with self.assertRaises(Exception):
            conn.ping()


class TestFileEntity(unittest.TestCase):
    def test_file_instance(self):
        file = File(None, None)

        with self.assertRaises(Exception):
            file.get(1)

        self.assertEqual(type(un.file), type(file))
        self.assertIsInstance(file, File)


class TestCheckEntity(unittest.TestCase):
    def test_check_instance(self):
        check = Check(None, None)

        with self.assertRaises(Exception):
            check.create(1, "web", 1, 1)

        self.assertEqual(type(un.check), type(check))
        self.assertIsInstance(check, Check)


if __name__ == "__main__":
    unittest.main()
