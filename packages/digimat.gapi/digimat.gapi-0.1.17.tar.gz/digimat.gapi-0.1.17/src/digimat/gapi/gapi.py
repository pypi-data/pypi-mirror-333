#!/usr/bin/env python
from __future__ import print_function

import logging
import sys

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
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

    @property
    def credentials(self):
        return self._credentials

    def reauth(self):
        credentials=self._credentials
        if credentials and credentials.valid:
            return credentials

        if os.path.exists(self._credentialsFile):
            with open (self._credentialsFile, 'rb') as f:
                credentials=pickle.load(f)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials=self.createInitialCredentials()

            with open(self._credentialsFile, 'wb') as f:
                pickle.dump(credentials, f)

            self._credentials=credentials

        return self._credentials

    def auth(self, clientId, clientSecret, host='127.0.0.1', port=8080):
        cient_config = { 'web':
            {
                'client_id': clientId,
                'client_secret': clientSecret,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token'
            }
        }

        with fopen(self._secretsFile, 'w') as f:
            f.write(json.dumps(client_config))

        flow=InstalledAppFlow.from_client_secrets_file(self._secretsFile,
            scopes=self._scopes)

        # be sure to allow redirect domain "http://127.0.0.1:8080/" in the google console
        credentials=app_flow.run_local_server(host=host, port=port)
        if credentials is not None:
            self._credentials=credentials
            with fopen(self._credentialsFile, 'w') as f:
                fwrite(f, credentials.to_json())
            return True
        return False

    def service(self, name, version):
        # TODO: check if this has to be adapted
        # -> https://github.com/googleapis/google-api-python-client/blob/main/UPGRADING.md
        return build(serviceName=name, version=version, http=self._http)


if __name__ == '__main__':
    pass
