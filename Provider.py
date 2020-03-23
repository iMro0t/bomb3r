import requests
import urllib3
import json
import random

DEFAULT_TIMEOUT = 30
VERIFY = True
not VERIFY and urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('config.json', 'r') as f:
    PROVIDERS = json.load(f)['providers']

class Provider:

    def __init__(self, target, proxy={}, verbose=False, cc='91', config=False):
        if config:
            self.config = config
        else:
            self.config = random.choice(PROVIDERS[cc if cc in PROVIDERS else 'multi'])
        self.target = target
        self.headers = self._headers()
        self.done = False
        self.proxy = proxy
        self.verbose = verbose
        self.cc = cc

    def _headers(self):
        tmp_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"}
        if 'headers' in self.config:
            tmp_headers.update(self.config['headers'])
        return tmp_headers

    def _data(self):
        data = self.config['data']
        if 'cc_target' in self.config:
            data[self.config['cc_target']] += self.cc
        data[self.config['target_param']] += self.target
        return data

    def _get(self):
        url = self.config['url'] + self.target
        if 'cc_target' in self.config:
            url += '&' + self.config['cc_target'] + '=' + self.cc
        return requests.get(url, headers=self.headers, timeout=DEFAULT_TIMEOUT, proxies=self.proxy, verify=VERIFY)

    def _post(self):
        if 'data_type' in self.config and self.config['data_type'].lower() == "json":
            return requests.post(self.config['url'], json=self.data, headers=self.headers, timeout=DEFAULT_TIMEOUT, proxies=self.proxy, verify=VERIFY)
        else:
            return requests.post(self.config['url'], data=self.data, headers=self.headers, timeout=DEFAULT_TIMEOUT, proxies=self.proxy, verify=VERIFY)

    def start(self):
        if self.config['method'] == 'GET':
            self.resp = self._get()
        elif self.config['method'] == 'POST':
            self.data = self._data()
            self.resp = self._post()
        self.done = True

    def status(self):
        if self.config['identifier'] in self.resp.text:
            self.verbose and print(
                '{:12}: success'.format(self.config['name']))
            return True
        else:
            self.verbose and print('{:12}: failed'.format(self.config['name']))
            return False
