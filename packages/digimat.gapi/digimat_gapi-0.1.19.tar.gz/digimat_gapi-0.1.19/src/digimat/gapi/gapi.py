#!/usr/bin/env python
from __future__ import print_function

import logging
import sys
import json
import webbrowser

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request


class GoogleAPI(object):
    def __init__(self, name, scopes, secretsFile='secrets.json', credentialsFile='credentials.dat'):
        logging.basicConfig(level=logging.INFO)
        self._name=name
        self._scopes=scopes
        self._secretsFile=secretsFile
        self._credentialsFile=credentialsFile
        self._credentials = None

    @property
    def name(self):
        return self._name

    def validateCredentials(self, credentials):
        try:
            if credentials is not None and credentials.valid and not credentials.expired:
                return True
        except:
            pass
        return False

    def refresh(self):
        credentials=self._credentials
        if credentials is not None and credentials.refresh_token:
            credentials.refresh(Request())
            if self.validateCredentials(credentials):
                return True
        return False

    def storeCredentials(self, credentials):
        self._credentials=credentials
        with open(self._credentialsFile, 'wb') as f:
            pickle.dump(credentials, f)

    def auth(self):
        credentials=self._credentials
        if self.validateCredentials(credentials):
            return credentials

        if credentials is None:
            try:
                if os.path.exists(self._credentialsFile):
                    with open (self._credentialsFile, 'rb') as f:
                        credentials=pickle.load(f)
            except:
                pass

        if self.validateCredentials(credentials):
            self._credentials=credentials
            return self._credentials

        if self.refresh():
            self.storeCredentials(credentials)
            return self._credentials

        self._credentials=None
        return None

    def reauth(self, redirect='https://www.digimat.ch/phpdev/site/gapi-auth.php'):
        # Add redirect to the authorized redirect urls on the google app console
        # -->https://www.digimat.ch/phpdev/site/gapi-auth.php
        flow = Flow.from_client_secrets_file(
            self._secretsFile, scopes=self._scopes, redirect_uri=redirect)

        authorization_url, state = flow.authorization_url(
            access_type="offline", prompt="consent"
        )

        # print(authorization_url)
        webbrowser.open(authorization_url)

        authorization_code=input('Code: ')
        if authorization_code:
            flow.fetch_token(code=authorization_code)

        credentials=flow.credentials
        if credentials.valid:
            self.storeCredentials(credentials)
            return credentials

    def service(self, name, version):
        credentials=self.auth()
        if credentials is not None:
            return build(serviceName=name, version=version, credentials=credentials)


if __name__ == '__main__':
    pass
