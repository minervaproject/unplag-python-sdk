import unittest
import responses

from requests_oauthlib import OAuth1Session
from unicheck.file import File

#   Initialize empty file entity
file = File(OAuth1Session('key', 'secret'), 'https://unicheck.com')


class TestFullFileEntity(unittest.TestCase):
    def test_file_abstract(self):
        self.assertIsInstance(file, File)
        self.assertIsInstance(file.oauth_session, OAuth1Session)
        self.assertEqual(file.server, 'https://unicheck.com')

    @responses.activate
    def test_mock_delete(self):
        responses.add(responses.POST, 'https://unicheck.com/api/v2/file/delete',
                 body='{"result": true}', status=200,
                 content_type='application/json')

        resp = file.delete(1)

        assert resp.status_code == 200
        assert resp.url == file.server + '/api/v2/file/delete'
        assert resp.text == '{"result": true}'

    @responses.activate
    def test_mock_get(self):
        responses.add(responses.GET, 'https://unicheck.com/api/v2/file/get',
                      body='{"result": true}', status=200,
                      content_type='application/json')

        resp = file.get(100500)

        assert resp.status_code == 200
        assert resp.url == file.server + '/api/v2/file/get?id=100500'
        assert resp.text == '{"result": true}'


if __name__ == "__main__":
    unittest.main()
