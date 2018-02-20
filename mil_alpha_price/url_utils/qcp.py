import urllib.parse
from html.parser import HTMLParser
import mil_alpha_price.common as common
from . import HOME_URL
from . import alpha

def get_qcp_form(alpha_url):
    content = common.http_get(alpha_url).decode('utf-8')

    hp = _HP()
    hp.feed(content)
    assert(hp.form is not None)

    return hp.form

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

    alpha_url = alpha.get_alpha_url(HOME_URL)
    
    qcp_form = get_qcp_form(alpha_url)
    
    print(qcp_form)
