import urllib.parse
from html.parser import HTMLParser
import mil_alpha_price.common as common
from . import HOME_URL

def get_alpha_url(home_url):
    content = common.http_get(home_url).decode('utf-8')
    hp = _HP()
    hp.feed(content)
    url_list = hp.url_list
    assert(len(url_list)==1)
    url = url_list[0]
    url = urllib.parse.urljoin(home_url, url)
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
    print(get_alpha_url(HOME_URL))
