from mil_alpha_price import common
from . import HOME_URL
from . import alpha, qcp
import os
import requests

if __name__ == '__main__':
    DIR=os.path.join(os.path.dirname(__file__),'references')
    
    common.reset_dir(DIR)

    cookies = requests.cookies.RequestsCookieJar()

    r = requests.get(HOME_URL, cookies=cookies)
    cookies.update(r.cookies)
    common.write(r.content, os.path.join(DIR,'home.txt'))
    alpha_url = alpha.parse_alpha_url(r)
    
    r = requests.get(alpha_url, cookies=cookies)
    cookies.update(r.cookies)
    common.write(r.content, os.path.join(DIR,'alpha.txt'))
    qcp_form = qcp.parse_qcp_form(r)

    print(cookies)

    r = requests.post(qcp_form['url'], data=qcp_form['data'], headers=qcp_form['headers'], cookies=cookies)
    common.write(r.content, os.path.join(DIR,'qcp.txt'))
