"""
This module represents file abstraction in Unicheck.
"""

from os.path import splitext
from msgpack import packb

from .response import UnicheckMainException
from .response import UnicheckFileResponse


class File(object):
    """ Representation of file abstact in Unicheck """

    def __init__(self, oauth_session, server):
        self.oauth_session = oauth_session
        self.server = server

    def delete(self, id):
        """
        Delete file from library

        :param id: file id in library, string or int
        :return: UnicheckFileResponse
        """
        resp = self.oauth_session.post(self.server + '/api/v2/file/delete', data={'id': id})
        return UnicheckFileResponse(resp)

    def get(self, id):
        """
        Get file info from library

        :param id: file id in library, string or int
        :return: UnicheckFileResponse
        """
        resp = self.oauth_session.get(self.server + '/api/v2/file/get?id=%s' % id)
        return UnicheckFileResponse(resp)

    def upload(self, path, upload_type='multipart', timeout=600, **kwargs):
        """
        Upload file to library

        :param path: full or absolute path to file
        :param upload_type: allowed upload using 'msgpack', 'multipart'
                            default is multipart
        :param timeout: timeout for uploading file,
                        default is 600 seconds (10 minutes)
        :param kwargs: optional arguments like directory_id='12820', name="Example name"
        :return: UnicheckFileResponse
        """

        def get_file_extension(path):
            _, file_ext = splitext(path)
            file_ext = file_ext.replace('.', '')
            return file_ext

        file_ext = get_file_extension(path)

        upload_url = self.server + '/api/v2/file/upload'

        # Switch-case for type of upload
        if upload_type == 'multipart':
            # This path used to be handled using a MultipartEncoder object
            # provided by the requests_toolbelt library, but the upgrade of
            # picasso to python 3.10 (see https://github.com/minervaproject/picasso/pull/11259)
            # required the removal of requests_toolbelt, since there was no
            # updated version of it that would be compatible. This code path
            # is unused by picasso (in fact, the whole File API is unused),
            # so we opt to just raise an exception here and move on with
            # our lives.
            raise Exception("Multipart uploads are no longer supported.")

        elif upload_type == 'msgpack':
            params = {'format': file_ext, 'file': open(path, 'rb').read()}
            params.update(kwargs)
            file = packb(params)
            resp = self.oauth_session.post(upload_url, data=file, headers={'Content-Type':  'application/x-msgpack'}, timeout=timeout)

        else:
            raise UnicheckMainException('Upload type not found!')

        return UnicheckFileResponse(resp)
