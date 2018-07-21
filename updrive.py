#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START import_libraries]
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseUpload, BytesIO
from time import sleep
# [END import_libraries]

"""
Shows basic usage of the Drive v3 API.
Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""


# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive v3 API
results = service.files().list().execute()
items = results.get('files', [])
myfile = None
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        if item['name'] == 'Speech To Text':
            print(item['name'])
            myfile = item
if not myfile:
    file_metadata = {
    'name': 'Speech To Text',
    'mimeType': 'application/vnd.google-apps.docs'
    }
    media = MediaFileUpload('start.txt',
                    # mimetype='text/txt',
                    resumable=True)
    myfile = service.files().create(body=file_metadata,
                    media_body=media,
                    fields='id').execute()
def updatefile(text):
    # file_metadata = {
    #     'name': 'Speech To Text',
    #     'mimeType': 'application/vnd.google-apps.docs'
    # }
    # ftu = 'start.txt'
    # with open('start.txt', 'r') as fi :
    #     if fi.read() == '':
    #         ftu = 'space.txt'
    print(text)
    bytes = BytesIO(text)
    media = MediaIoBaseUpload(bytes,
                mimetype='text/',
                resumable=True)
    updatedfile = service.files().update(fileId=myfile['id'], media_body=media,
                fields='id').execute()
