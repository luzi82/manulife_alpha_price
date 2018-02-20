import urllib.parse
from html.parser import HTMLParser
import mil_alpha_price.common as common

def parse_qcp_form(r):
    content = r.text

    hp = _HP()
    hp.feed(content)
    assert(hp.form is not None)
    form = hp.form

    url = form['attr_dict']['action']
    url = urllib.parse.urljoin(r.url, url)
    
    data = {}
    for attr_dict in form['input_attr_dict_list']:
        if 'name' not in attr_dict:
            continue
        if 'value' in attr_dict:
            value = attr_dict['value']
        elif ('type' in attr_dict) and (attr_dict['type']=='submit'):
            value = 'Submit'
        else:
            value = ''
        name = attr_dict['name']
        data[name] = value
        
    headers = {}
    headers['Referer'] = r.url

    return {
        'url':url,
        'data':data,
        'headers':headers,
    }

def attrs_to_dict(attrs):
    return {k:v for k,v in attrs}

class _HP(HTMLParser):

    def __init__(self):
        super().__init__()
        self.form = None
        self.form_active = False

    def handle_starttag(self, tag, attrs):
        if tag == 'form':
            attr_dict=attrs_to_dict(attrs)
            if 'aplhaGroupNavigation' in attr_dict['id']:
                assert(self.form is None)
                assert(not self.form_active)
                self.form = {}
                self.form_active = True

                self.form['input_attr_dict_list'] = []
                self.form['attr_dict'] = attr_dict
        if self.form_active and tag == 'input':
            attr_dict=attrs_to_dict(attrs)
            self.form['input_attr_dict_list'].append(attr_dict)

    def handle_endtag(self, tag):
        if self.form_active and tag == 'form':
            self.form_active = False

if __name__ == '__main__':
    from . import HOME_URL
    from . import alpha

    import requests
    
    cookies = requests.cookies.RequestsCookieJar()
    
    r = requests.get(HOME_URL, cookies=cookies)
    alpha_url = alpha.parse_alpha_url(r)

    r = requests.get(alpha_url, cookies=cookies)
    qcp_form = parse_qcp_form(r)
    
    print(qcp_form)
    