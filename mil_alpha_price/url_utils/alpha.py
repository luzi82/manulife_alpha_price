import urllib.parse
from html.parser import HTMLParser
import mil_alpha_price.common as common

def parse_alpha_url(r):
    hp = _HP()
    hp.feed(r.text)
    url_list = hp.url_list
    assert(len(url_list)==1)
    url = url_list[0]
    url = urllib.parse.urljoin(r.url, url)
    return url

class _HP(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tmp_url=None
        self.url_list=[]
    def handle_starttag(self, tag, attrs):
        if tag!='a':
            return
        for k,v in attrs:
            if k!='href':
                continue
            self.tmp_url=v
            return
        self.tmp_url=None
    def handle_data(self, data):
        if self.tmp_url is None:
            return
        data=data.strip()
        if data!='Alpha':
            return
        self.url_list.append(self.tmp_url)

if __name__ == '__main__':
    from . import HOME_URL
    import requests
    
    cj = requests.cookies.RequestsCookieJar()
    
    r = requests.get(HOME_URL, cookies=cj)
    print(parse_alpha_url(r))
