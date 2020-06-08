"""
This module represents check abstraction in Unplag.
"""

from time import sleep

from .response import UnplagCheckResponse


class Check(object):
    """ Representation of Check abstact in Unplag """

    def __init__(self, oauth_session, server):
        self.oauth_session = oauth_session
        self.server = server

    def create(self, file_id, type='web', exclude_citations=0, exclude_references=0):
        """
        Start check for file id

        :param file_id: int
        :param type: respesents type of check, alowed is
                    "my_library", "web", "external_database", "doc_vs_docs", "web_and_my_library"
        :param exclude_citations: boolean
        :param exclude_references: boolean
        :return: UnplagCheckResponse
        """

        parameters = {
            "type": type,
            "file_id": file_id,
            "exclude_citations": exclude_citations,
            "exclude_references": exclude_references
        }

        resp = self.oauth_session.post(self.server + '/api/v2/check/create', data=parameters)
        return UnplagCheckResponse(resp)

    def create_sync(self, *args, **kwargs):
        """
        Advanced method, wraps default API to make synchronous check
        Start check and wait for it completion
        Params similar to create method

        :param args: pass to create method file id
        :param kwargs: pass to create method other parameters
        :return: UnplagCheckResponse
        """

        check = self.create(*args, **kwargs)

        check_id = check.response['check']['id']
        progress = check.response['check']['progress']

        while progress < 1:
            progress_resp = self.track_progress(check_id)
            progress = progress_resp.response['progress'][str(check_id)]
            sleep(5)

        return self.get(check_id)

    def delete(self, id):
        """
        Delete check for check id

        :param id: check id (string or int)
        :return: UnplagCheckResponse
        """

        resp = self.oauth_session.post(self.server + '/api/v2/check/delete', data={"id": id})
        return UnplagCheckResponse(resp)

    def generate_pdf(self, id, lang="en_EN"):
        """
        Generate pdf for check id

        :param id: finished check id
        :param lang: main report language "en_EN", "uk_UA", "es_ES", "nl_BE"
        :return: UnplagCheckResponse
        """

        resp = self.oauth_session.post(self.server + '/api/v2/check/generate_pdf', data={"id": id, "lang": lang})
        return UnplagCheckResponse(resp)

    def get(self, id):
        """
        Get info about check

        :param id: check id
        :return: UnplagCheckResponse
        """

        resp = self.oauth_session.get(self.server + '/api/v2/check/get?id=%s' % id)
        return UnplagCheckResponse(resp)

    def get_report_link(self, id, lang='en_EN', show_lang_picker=0):
        """
        Get report link in preffered language

        :param id: check id
        :param lang: check report language, allowed is en_EN, uk_UA, es_ES, nl_BE
        :param show_lang_picker: bool
        :return: UnplagCheckResponse
        """

        resp = self.oauth_session.get(self.server + '/api/v2/check/get_report_link?id=%s&lang=%s&show_lang_picker=%s' % (id, lang, show_lang_picker))
        return UnplagCheckResponse(resp)

    def toogle_citations(self, id, exclude_citations, exclude_references):
        """
        Exclude citations or references for check

        :param id: check id
        :param exclude_citations: bool
        :param exclude_references: bool
        :return: UnplagCheckResponse
        """

        parameters = {
            "id": id,
            "exclude_citations": exclude_citations,
            "exclude_references": exclude_references
        }

        resp = self.oauth_session.post(self.server + '/api/v2/check/toggle', data=parameters)
        return UnplagCheckResponse(resp)

    def track_progress(self, id):
        """
        Track progress for check

        :param id: check id
        :return: UnplagCheckResponse
        """

        resp = self.oauth_session.get(self.server + '/api/v2/check/progress?id=%s' % id)
        return UnplagCheckResponse(resp)