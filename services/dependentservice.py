from utils.requester import Requester


class DependentService:
    def __init__(self, host, auth_token, timeout, retries, cache_ttl=0):
        self.host = host
        self.auth_token = auth_token
        self.timeout = timeout
        self.retries = retries
        self.cache_ttl = cache_ttl
        self.requester = Requester(auth_token=self.auth_token,
                                   retries=retries,
                                   timeout=timeout,
                                   cache_ttl=cache_ttl)

    def get(self, url):
        return self.requester.get(url=url)

    def post(self, url, content):
        return self.requester.post(url=url, content=content)
