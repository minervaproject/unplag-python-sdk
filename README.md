Unicheck Python Library
===================

This library eases the use of the Unicheck REST API from Python and it has been used in production for years.

As this is an open-source project that is community maintained, do not be surprised if some bugs or features are not implemented quickly enough.

Quickstart
----------

Installation

    sudo pip install unicheck

Feeling impatient? I like your style.

    from unicheck import Unicheck

    un = Unicheck('api_key', 'api_secret')    # Creating connection

    upload = un.file.upload('~/Downloads/original.pdf')     # Upload file from path

    check = un.check.create_sync(upload_resp.response['file']['id'])    # Start check using upload id


Short syntax
------------

    from unicheck import Unicheck

    un = Unicheck('api_key', 'api_secret')

    un.check.create_sync(un.file.upload('~/Downloads/original.pdf').response['file']['id']).response
