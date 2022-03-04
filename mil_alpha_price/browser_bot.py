from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from mil_alpha_price import common
import os
import datetime
import shutil
import traceback
import time
import gc
import re
import sys
import argparse
import futsu.csv

parser = argparse.ArgumentParser()
parser.add_argument('firefox_bin', nargs='?')
args = parser.parse_args()

args_firefox_bin = args.firefox_bin if args.firefox_bin else '/usr/bin/firefox'

def find_file(dir):
    file_list = []
    for root, _, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def find_fund_file(code):
    file_list = find_file('tmp')
    file_list = filter(lambda i:i.startswith(f'tmp/Manulife-Fund-{code}_'), file_list)
    file_list = list(file_list)
    if len(file_list) == 0 : return None
    if len(file_list) == 1 : return file_list[0]
    assert(False)

FirefoxProfile = webdriver.firefox.firefox_profile.FirefoxProfile

def get_fund_list(driver):
    try:
        print('HDCGJJJL')
        tbody_list = driver.find_elements_by_tag_name('tbody')
        print('KHYWUEHA {}'.format(len(tbody_list)))
        tbody_list = list(filter(lambda _ele: ':mainContentForm:' in _ele.get_attribute('id'),tbody_list))
        print('TKOCDUME {}'.format(len(tbody_list)))
        fund_list = []
        for tbody in tbody_list:
            print('VMCITYUP')
            tr_list = tbody.find_elements_by_tag_name('tr')
            for tr in tr_list:
                td_list = tr.find_elements_by_tag_name('td')
                a_list  = tr.find_elements_by_tag_name('a')
                code = str(td_list[0].text)
                name = str(td_list[1].text)
                #link = str(a_list[2].get_attribute('id'))
                link = a_list[2]
                #print(code)
                fund_list.append({
                    'code':code,
                    'name':name,
                    'link':link,
                })
            print('BUFXQVOH')
        return fund_list
    except:
        return None

def fix_fund_name(name):
    name = re.sub('[^0-9a-zA-Z ]','',name)
    name = name.strip()
    return name

def wait_stale(ele):
    try:
        while True:
            ele.is_enabled()
            time.sleep(1)
    except selenium.common.exceptions.StaleElementReferenceException as e:
        pass

ret_code = 0

today_dt = datetime.date.today()
yyyymmdd_end = today_dt.strftime('%Y/%m/%d')
yyyymmdd_start = (today_dt-datetime.timedelta(days=29)).strftime('%Y/%m/%d')

common.reset_dir('profile')
common.reset_dir('tmp')
common.reset_dir('output')

profile = FirefoxProfile('profile')
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", os.path.join(os.getcwd(),'tmp'))

driver = None

try:
    driver = webdriver.Firefox(firefox_profile=profile, executable_path='tmp_0/geckodriver', firefox_binary=args_firefox_bin)
    
    HOME_URL = 'https://www.manulife.com.hk/en/individual/fund-price/investment-linked-assurance-scheme.html/v2?product=Alpha'
    print(f'AXNGEAIBEW go {HOME_URL}')
    driver.get(HOME_URL)
    time.sleep(1)
    
    print('SCLASBLR Detect Agree button')
    while True:
        ele_list = driver.find_elements_by_tag_name('button')
        ele_list = filter(lambda _ele:_ele.text.strip() == 'Agree', ele_list)
        #ele_list = filter(lambda _ele:'cmp-link-disclaimer__modal-content' in _ele.get_attribute('class').strip(), ele_list)
        #ele_list = filter(lambda _ele:'cmp-modal__content' in _ele.get_attribute('class').strip(), ele_list)
        ele_list = list(ele_list)
        print(f'len(ele_list)={len(ele_list)}')
        if (len(ele_list)>0): break
        time.sleep(1)
    assert(len(ele_list)==1)
    ele = ele_list[0]
    
    print('VZTTTYLO Enable Agree button')
    driver.execute_script('$(".cmp-modal__button-confirm").removeClass("disabled");');
    time.sleep(1)

    print('ZKLVTKER click <button> Agree')
    # ele.send_keys(Keys.RETURN)
    driver.execute_script('$(".cmp-modal__button-confirm").click();');
    time.sleep(1)
    print('EDSNQPTC click <button> Agree done')

    url_list = []
    
    #PREFIX = 'https://www.manulife.com.hk/en/individual/fund-price/investment-linked-assurance-scheme.html/v2/funddetails/'
    PATTERN = 'https://www\.manulife\.com\.hk/en/individual/fund-price/investment-linked-assurance-scheme.html/v2/funddetails/(.+)\?product=Alpha'

    _url_list = driver.find_elements_by_tag_name('a')
    _url_list = filter(lambda _ele:_ele.get_attribute('href') is not None, _url_list)
    _url_list = filter(lambda _ele:re.fullmatch(PATTERN, _ele.get_attribute('href').strip()) is not None, _url_list)
    _url_list = map(lambda _ele:_ele.get_attribute('href').strip(), _url_list)
    _url_list = list(_url_list)
    url_list += _url_list
    
    page_number = 2
    while True:
        print(f'page_number={page_number}')
        ele_list = driver.find_elements_by_tag_name('a')
        ele_list = filter(lambda _ele:_ele.text.strip() == str(page_number), ele_list)
        ele_list = filter(lambda _ele:_ele.get_attribute('_ngcontent-c14') is not None, ele_list)
        ele_list = list(ele_list)
        # print(f'len(ele_list)={len(ele_list)}')
        if len(ele_list) == 0: break
        ele = ele_list[0]
        driver.execute_script('arguments[0].click();', ele);
        time.sleep(1)

        _url_list = driver.find_elements_by_tag_name('a')
        _url_list = filter(lambda _ele:_ele.get_attribute('href') is not None, _url_list)
        _url_list = filter(lambda _ele:re.fullmatch(PATTERN, _ele.get_attribute('href').strip()) is not None, _url_list)
        _url_list = map(lambda _ele:_ele.get_attribute('href').strip(), _url_list)
        _url_list = list(_url_list)
        url_list += _url_list

        page_number += 1
    
    print(f'WRGQUIIX len(url_list)={len(url_list)}')
    print(f'ZWQGADMV url_list={url_list}')
    
    for url in url_list:
        print(f'url={url}')
        code = re.fullmatch(PATTERN, url).group(1)
        print(f'code={code}')
        download_done = False
        lessthansixmonth_exist = False
        for _i in range(3): # try download 3 times
        
            # clear old file
            fn = find_fund_file(code)
            if fn is not None:
                os.remove(fn)
        
            driver.get(url)
            time.sleep(5)
            
            print('UKXLUOUQ Detect if less than six month')
            for _ in range(5):
                try:
                    ele_list = driver.find_elements_by_tag_name('div')
                    ele_list = filter(lambda _ele:'historical-nav__lessthansixmonth' in _ele.get_attribute('class').strip(), ele_list)
                    ele_list = list(ele_list)
                    if (len(ele_list)>0): break
                    time.sleep(1)
                except:
                    pass
            
            if len(ele_list) == 0: continue
            assert(len(ele_list)==1)
            
            ele = ele_list[0]
            if 'hidden' not in ele.get_attribute('class').strip():
                lessthansixmonth_exist = True
                break
            
            print('VLAPGUVJ Detect [Export data] button')
            for _ in range(5):
                ele_list = driver.find_elements_by_tag_name('button')
                ele_list = filter(lambda _ele:_ele.text.strip() == 'Export data', ele_list)
                ele_list = list(ele_list)
                if (len(ele_list)>0): break
                time.sleep(1)
                
            if len(ele_list) == 0: continue
            assert(len(ele_list)==1)
            
            ele = ele_list[0]
            
            print('WZLMHHHH Click [Export data] button')
            driver.execute_script('arguments[0].click();', ele);
            time.sleep(1)
            
            print('NCSYWBKR Detect [Export to .csv] input')
            ele = None
            for _ in range(5):
                try:
                    ele = driver.find_element_by_id('csv')
                    break
                except:
                    ele = None
                    pass
                time.sleep(1)
    
            if ele is None: continue
            
            print('QVKURDJC Click [Export to .csv] input')
            driver.execute_script('arguments[0].click();', ele);
            time.sleep(1)
    
            print('WFFPVAQM Detect [Export] button')
            for _ in range(5):
                ele_list = driver.find_elements_by_tag_name('button')
                ele_list = filter(lambda _ele:_ele.text.strip() == 'Export', ele_list)
                ele_list = list(ele_list)
                if (len(ele_list)>0): break
                time.sleep(1)
            
            if len(ele_list) == 0: continue
            assert(len(ele_list)==1)
            
            ele = ele_list[0]
            
            print('QFIEBZPX Click [Export] button')
            driver.execute_script('arguments[0].click();', ele);
            time.sleep(1)
    
            # wait file exist
            for _ in range(5):
                fn = find_fund_file(code)
                if fn is not None:
                    break
                time.sleep(1)
            
            if fn is None:
                print(f'KTAJXGCX output file not found, code={code}')
                continue
            
            # wait file size > 0
            file_size = 0
            for _ in range(5):
                file_size = os.path.getsize(fn)
                if file_size > 0:
                    break
                time.sleep(1)

            if file_size == 0:
                print(f'KMQBBCBN file_size == 0: code={code}')
                continue

            # wait file size stop grow
            while True:
                time.sleep(5)
                file_size_tmp = os.path.getsize(fn)
                if file_size_tmp == file_size:
                    break
                file_size = file_size_tmp
            
            download_done = True
            break

        if lessthansixmonth_exist:
            time.sleep(1)
            continue

        assert(download_done)

        shutil.move(fn, os.path.join('output',f'{code}.csv'))

        print('QTHAEJNF download end: {}'.format(code))

        time.sleep(1)

except Exception:
    ret_code = 1
    traceback.print_exc()

if driver is not None:
    driver.close()

sys.exit(ret_code)
