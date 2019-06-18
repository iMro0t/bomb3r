import requests
import json,random


### HEADERS ###
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0","Accept":"*/*","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}

### CONFIG ###
CONFIG = {"version": 1.0, "created_by": "iMro0t", "credits": ["InsideU", "bhattsameer", "KANG-NEWBIE"], "providers": [{"name": "confirmtkt", "method": "GET", "type": "HTTPS", "multi": False, "url": "securedapi.confirmtkt.com/api/platform/register?newOtp=true&mobileNumber=", "identifier": "false", "last_modified": "2019-05-20"}, {"name": "justdial", "method": "GET", "type": "HTTPS", "multi": False, "url": "t.justdial.com/api/india_api_write/18july2018/sendvcode.php?mobile=", "identifier": "sent", "last_modified": "2019-05-20"}, {"name": "oyorooms", "method": "GET", "type": "HTTPS", "multi": False, "url": "www.oyorooms.com/api/pwa/generateotp?country_code=91&nod=4&phone=", "identifier": "correct", "last_modified": "2019-05-20"}]}

class Provider:
    global headers,CONFIG
    def __init__(self, target):
        self.config = CONFIG['providers'][random.randint(0,2)]
        #self.config = json.load(open('original.json','r'))['providers'][random.randint(0,2)]
        self.target = target
        self.headers = self._headers()
        self.method = self.config['method']
        self.url = self.config['type'].lower()+'://'+self.config['url']     
        self.identifier = self.config['identifier']
        self.done = False

    def _headers(self):
        tmp_headers = {key:value for key,value in headers.items()}
        if 'headers' in self.config:
            for key,value in self.config['headers'].items():
                tmp_headers[key] = value
        if 'data_type' in self.config and self.config['data_type'].lower()=="json": 
            tmp_headers['Content-Type']='application/json'
            self.data_type = 'json'
        else:
            tmp_headers['Content-Type']='application/x-www-form-urlencoded'
            self.data_type = 'urlencoded'
        return tmp_headers
    
    def _data(self):
        data = self.config['data']
        if self.config['multi']:
            data[self.config['cc_target']]+='91'
        data[self.config['target_param']]+=self.target
        return data
    
    def _get(self):
        return requests.get(self.url+self.target, headers=self.headers, timeout=10)

    def _post(self):
        if self.data_type == "json":        
            return requests.post(self.url, json=self.data, headers=self.headers, timeout=10)
        elif self.data_type == "urlencoded":
            return requests.post(self.url, data=self.data, headers=self.headers, timeout=10)

    def start(self):
        if self.method == 'GET':
            self.resp = self._get()
        elif self.method == 'POST':
            self.data = self._data()
            self.resp = self._post()
        self.done = True
    
    def status(self):
        if self.resp == None:
            return None
        elif self.identifier in self.resp.text:
            return True
        else:
            self.log = {self.config['name']:self.resp.text}
            return False
    
