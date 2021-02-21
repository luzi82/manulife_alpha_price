HOME_URL='https://fundprice.manulife.com.hk/wps/portal/pwsdfphome/dfp/detail?catId=11&locale=en'

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
    
    print(f'AXNGEAIBEW go {HOME_URL}')
    driver.get(HOME_URL)
    time.sleep(1)
    
    while True:
        ele_list = driver.find_elements_by_tag_name('a')
        ele_list = list(filter(lambda _ele:_ele.text.strip() == 'Alpha', ele_list))
        if (len(ele_list)>0): break
        time.sleep(1)
    assert(len(ele_list)==1)
    ele = ele_list[0]
    
    print('CDWZVMPJZF click <a> Alpha')
    ele.send_keys(Keys.RETURN)
    print('QGEOWRQYFE click <a> Alpha done')
    time.sleep(1)

    while len(driver.find_elements_by_id('wpthemeComplementaryContent')) == 0:
        time.sleep(1)
    
    while True:
        try:
            ele_list = driver.find_elements_by_tag_name('input')
            ele_list = list(filter(lambda _ele:_ele.get_attribute('value').strip() == 'I have read and understood the above information', ele_list))
            if len(ele_list) > 0:
                break
        except:
            pass
    
    assert(len(ele_list)==1)
    ele = ele_list[0]
    
    while not ele.is_displayed():
        pass

    ele.send_keys(Keys.RETURN)
    
    #index_url = driver.current_url
    #print(index_url)
    
    time.sleep(5)
    fund_list = get_fund_list(driver)
    fund_code_list  = [ fund['code'] for fund in fund_list ]
    fund_code_list = list(sorted(fund_code_list))

    fund_code_name_dict = { fund['code']: fund['name'] for fund in fund_list }
    
    # driver.find_element_by_id(fund_list[0]['link']).send_keys(Keys.RETURN)
    fund_list[0]['link'].send_keys(Keys.RETURN)

    for fund_code in fund_code_list:
    
        print(f'GJJTXOLK fund_code={fund_code}')
    
        while True:
            try:
                input_list = driver.find_elements_by_tag_name('input')
                start_input_list = list(filter(lambda input:'startDateId' in input.get_attribute('id'),input_list))
                end_input_list   = list(filter(lambda input:'endDateId' in input.get_attribute('id'),input_list))
                view_input_list = list(filter(lambda input:'View Data' in input.get_attribute('value'),input_list))
                if len(start_input_list) <= 0:
                    continue
                if len(end_input_list) <= 0:
                    continue
                if len(view_input_list) <= 0:
                    continue
                break
            except:
                continue
    
        assert(len(start_input_list)==1)
        assert(len(end_input_list)==1)
        assert(len(view_input_list)==1)
        
        start_input = start_input_list[0]
        end_input   = end_input_list[0]
        view_input = view_input_list[0]
    
        start_input.clear()
        start_input.send_keys(yyyymmdd_start)
        end_input.clear()
        end_input.send_keys(yyyymmdd_end)
    
        option_list = driver.find_elements_by_tag_name('option')
        option_value_list = [ option.get_attribute('value') for option in option_list ]
        option_value_list = list(sorted(option_value_list))
        
        assert(fund_code_list==option_value_list)
    
        option = list(filter(lambda i:i.get_attribute('value')==fund_code, option_list))
        assert(len(option)==1)
        option = option[0]
    
        code = option.get_attribute('value')
        #print('NTHLNZEZ download start: {}'.format(code))

        csv_filename = os.path.join('tmp','fund.csv')
        if os.path.exists(csv_filename):
            os.remove(csv_filename)

        option.click()

        time.sleep(1)

        view_input.send_keys(Keys.RETURN)
        
        wait_stale(view_input)
        
        time.sleep(1)

        # wait data exist
        for _ in range(5):
            ele_list = driver.find_elements_by_tag_name('table')
            ele_list = list(filter(lambda _ele:_ele.get_attribute('role') == 'grid', ele_list))
            if len(ele_list)==2: break
            time.sleep(1)
        
        table_ele = ele_list[1]
        
        csv_data_list = []
        tr_list = table_ele.find_elements_by_tag_name('tr')
        for tr in tr_list[1:]:
            tr = tr_list[1]
            td_list = tr.find_elements_by_tag_name('td')
            assert(len(td_list)==4)
            csv_data_list.append({
                'Name of Investment Choice': fund_code_name_dict[code],
                'Date':            td_list[0].text,
                'Currency':        td_list[1].text,
                'Purchase Price':  td_list[2].text,
                'Unit Sell Price': td_list[3].text,
            })
        
        futsu.csv.write_csv(
            csv_filename,
            csv_data_list,
            ['Name of Investment Choice','Date','Currency','Purchase Price','Unit Sell Price'],
            ['Date']
        )
        
        shutil.move(os.path.join('tmp','fund.csv'), os.path.join('output','{}.csv'.format(code)))

        print(f'QTHAEJNF download end: {code}')

        time.sleep(1)

except Exception:
    ret_code = 1
    traceback.print_exc()

if driver is not None:
    driver.close()

sys.exit(ret_code)
