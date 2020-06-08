import unittest
import responses

from requests_oauthlib import OAuth1Session
from unicheck.directory import Directory

#   Initialize empty directory entity
folder = Directory(OAuth1Session('key', 'secret'), 'https://unicheck.com')


class TestFullFileEntity(unittest.TestCase):
    def test_directory_abstract(self):
        self.assertIsInstance(folder, Directory)

    @responses.activate
    def test_mock_directory_create(self):
        create_resp = '{"result": true, "errors": [], "directory": {"id": 41, "name": "Bruce Willis", "parent_id": 0 }}'

        responses.add(responses.POST, 'https://unicheck.com/api/v2/directory/create',
                 body=create_resp, status=200,
                 content_type='application/json')

        resp = folder.create("Bruce Willis")

        assert resp.status_code == 200
        assert resp.url == folder.server + '/api/v2/directory/create'
        assert resp.response['result'] == True
        assert resp.response['directory']['id'] == 41
        assert resp.response['directory']['name'] == 'Bruce Willis'
        assert resp.response['directory']['parent_id'] == 0

    @responses.activate
    def test_mock_directory_delete(self):
        delete_resp = '{"result": true, "errors": [], "id": 42 }'

        responses.add(responses.POST, 'https://unicheck.com/api/v2/directory/delete',
                 body=delete_resp, status=200,
                 content_type='application/json')

        resp = folder.delete(42)

        assert resp.status_code == 200
        assert resp.url == folder.server + '/api/v2/directory/delete'
        assert resp.response['result'] == True
        assert resp.response['id'] == 42

    @responses.activate
    def test_mock_directory_get(self):
        get_resp = '{"result": true, "errors": [], "directory": {"id": 0, "name": "root", "parent_id": null }, "list": {"directories": [{"id": 13, "name": "Chack Norris", "parent_id": 0 } ] } }'

        responses.add(responses.GET, 'https://unicheck.com/api/v2/directory/get',
                      body=get_resp, status=200,
                      content_type='application/json')

        resp = folder.get(0, True)

        assert resp.status_code == 200
        assert resp.url == folder.server + '/api/v2/directory/get?id=0?list=1'
        assert resp.response['result'] == True
        assert resp.response['directory']['id'] == 0
        assert resp.response['list']['directories'][0]['id'] == 13
        assert resp.response['list']['directories'][0]['name'] == 'Chack Norris'


if __name__ == "__main__":
    unittest.main()
