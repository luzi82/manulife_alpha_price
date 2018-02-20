from mil_alpha_price import common
from . import HOME_URL
from . import alpha
import os

if __name__ == '__main__':
    DIR=os.path.join(os.path.dirname(__file__),'references')
    
    common.reset_dir(DIR)

    common.download(HOME_URL,os.path.join(DIR,'home.txt'))
    
    alpha_url = alpha.get_alpha_url(HOME_URL)
    common.download(alpha_url,os.path.join(DIR,'alpha.txt'))
