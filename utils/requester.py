import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_cache import CachedSession
from model.error import Errors


class Requester(object):
    def __init__(self, auth_token, retries=0, timeout=0, cache_ttl=0, session=None):
        self.auth_token = auth_token
        self.default_header = {'Authorization': self.auth_token,
                               'Content-Type': 'application/json'}
        self.retries = retries
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        if session:
            self.session = session
            return
        if cache_ttl:
            self.session = CachedSession('Requester', expire_after=cache_ttl)
        else:
            self.session = requests.Session()

        retry = Retry(total=retries,
                      read=retries,
                      connect=retries,
                      backoff_factor=0.3,
                      status_forcelist=(500, 502, 504),)

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get(self, url):
        try:
            r = self.session.get(url=url, headers=self.default_header, timeout=self.timeout)
            if r.status_code != 200:
                return Errors.HTTP_STATUS.build_json(code=r.status_code), False
            if r.status_code == 200:
                return r.json(), True
        except requests.exceptions.Timeout:
            return Errors.REQUEST_TIMEOUT.build_json(), False
        except requests.exceptions.HTTPError:
            return Errors.HTTP_ERROR.build_json(), False
        except requests.exceptions.InvalidURL:
            return Errors.INVALID_URL.build_json(), False

    def post(self, url, content):
        try:
            r = self.session.post(url=url, headers=self.default_header, timeout=self.timeout, json=content)
            if r.status_code != 201:
                return Errors.HTTP_STATUS.build_json(code=r.status_code), False
            if r.status_code == 201:
                return r.json(), True
        except requests.exceptions.Timeout:
            return Errors.REQUEST_TIMEOUT.build_json(), False
        except requests.exceptions.HTTPError:
            return Errors.HTTP_ERROR.build_json(), False


