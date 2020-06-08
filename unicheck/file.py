"""
This module represents file abstraction in Unplag.
"""

from os.path import splitext
from requests_toolbelt import MultipartEncoder
from msgpack import packb

from .response import UnplagMainException
from .response import UnplagFileResponse


class File(object):
    """ Representation of file abstact in Unplag """

    def __init__(self, oauth_session, server):
        self.oauth_session = oauth_session
        self.server = server

    def delete(self, id):
        """
        Delete file from library

        :param id: file id in library, string or int
        :return: UnplagFileResponse
        """
        resp = self.oauth_session.post(self.server + '/api/v2/file/delete', data={'id': id})
        return UnplagFileResponse(resp)

    def get(self, id):
        """
        Get file info from library

        :param id: file id in library, string or int
        :return: UnplagFileResponse
        """
        resp = self.oauth_session.get(self.server + '/api/v2/file/get?id=%s' % id)
        return UnplagFileResponse(resp)

    def upload(self, path, upload_type='multipart', timeout=600, **kwargs):
        """
        Upload file to library

        :param path: full or absolute path to file
        :param upload_type: allowed upload using 'msgpack', 'multipart'
                            default is multipart
        :param timeout: timeout for uploading file,
                        default is 600 seconds (10 minutes)
        :param kwargs: optional arguments like directory_id='12820', name="Example name"
        :return: UnplagFileResponse
        """

        def get_file_extension(path):
            _, file_ext = splitext(path)
            file_ext = file_ext.replace('.', '')
            return file_ext

        file_ext = get_file_extension(path)

        upload_url = self.server + '/api/v2/file/upload'

        # Switch-case for type of upload
        if upload_type == 'multipart':
            params = {'format': file_ext, 'file': ('check', open(path, 'rb'), 'application/' + file_ext)}
            params.update(kwargs)
            file = MultipartEncoder(fields=params)
            resp = self.oauth_session.post(upload_url, data=file, headers={'Content-Type':  file.content_type}, timeout=timeout)

        elif upload_type == 'msgpack':
            params = {'format': file_ext, 'file': open(path, 'rb').read()}
            params.update(kwargs)
            file = packb(params)
            resp = self.oauth_session.post(upload_url, data=file, headers={'Content-Type':  'application/x-msgpack'}, timeout=timeout)

        else:
            raise UnplagMainException('Upload type not found!')

        return UnplagFileResponse(resp)
