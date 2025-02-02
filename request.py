##
# Copyright 2016 Jeffrey D. Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

import requests
from requests.exceptions import HTTPError

class Request(object):
    """HTTP helper class"""

    def __init__(self):
        self.session = requests.Session()

    def _request(self, url, method='GET', params={}, headers={}, stream=False, raw=False):
        if method == 'GET':
            r = self.session.get(url, params=params, headers=headers, stream=stream, timeout=60)
            if stream is True:
                return r
        elif method == 'PUT':
            r = self.session.put(url, json=params, headers=headers, timeout=60)
        elif method == 'POST':
            r = self.session.post(url, json=params, headers=headers, timeout=60)

        r.raise_for_status()
        body = r.json()

        if raw:
            return body
        else:
            if body['success'] == True:
                if 'data' in body:
                    return body['data']
            else:
                raise HTTPError('Request ({0} {1}) failed: {2}'.format(method, url, r.json()), response=r)

    def get(self, url, params={}, headers={}, stream=False, raw=False):
        return self._request(url, 'GET', params, headers, stream, raw)

    def put(self, url, params={}, headers={}, raw=False):
        return self._request(url, 'PUT', params, headers, raw)

    def post(self, url, params={}, headers={}, raw=False):
        return self._request(url, 'POST', params, headers, raw)
