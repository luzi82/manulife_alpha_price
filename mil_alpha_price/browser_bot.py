HOME_URL='https://www.manulife.com.hk/wps/portal/pwshome/dfp'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mil_alpha_price import common
import os
import datetime
import shutil
import traceback
import time
import gc

FirefoxProfile = webdriver.firefox.firefox_profile.FirefoxProfile

def get_fund_list(driver):
    try:
        print('HDCGJJJL')
        tbody_list = driver.find_elements_by_tag_name('tbody')
        print('KHYWUEHA {}'.format(len(tbody_list)))
        tbody_list = list(filter(lambda _ele: ':mainContent:' in _ele.get_attribute('id'),tbody_list))
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
                link = str(a_list[2].get_attribute('id'))
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

yyyymmdd = datetime.date.today().strftime('%Y/%m/%d')

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
    driver = webdriver.Firefox(firefox_profile=profile)
    
    driver.get(HOME_URL)
    
    ele_list = driver.find_elements_by_tag_name('a')
    ele_list = list(filter(lambda _ele:_ele.text.strip() == 'Alpha', ele_list))
    assert(len(ele_list)==1)
    ele = ele_list[0]
    
    ele.send_keys(Keys.RETURN)

    time.sleep(1)
    while len(driver.find_elements_by_id('wpthemeComplementaryContent')) == 0:
        pass
    
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

    index_url = driver.current_url
    print(index_url)
    
    time.sleep(5)
    fund_list = get_fund_list(driver)
    fund_code_list  = [ fund['code'] for fund in fund_list ]
    fund_code_list = list(sorted(fund_code_list))
    
    driver.find_element_by_id(fund_list[0]['link']).send_keys(Keys.RETURN)
    
    while True:
        try:
            input_list = driver.find_elements_by_tag_name('input')
            start_input_list = list(filter(lambda input:'startDateId' in input.get_attribute('id'),input_list))
            end_input_list   = list(filter(lambda input:'endDateId' in input.get_attribute('id'),input_list))
            download_input_list = list(filter(lambda input:'Download Data' in input.get_attribute('value'),input_list))
            if len(start_input_list) <= 0:
                continue
            if len(end_input_list) <= 0:
                continue
            if len(download_input_list) <= 0:
                continue
            break
        except:
            continue

    assert(len(start_input_list)==1)
    assert(len(end_input_list)==1)
    assert(len(download_input_list)==1)
    
    start_input = start_input_list[0]
    end_input   = end_input_list[0]
    download_input = download_input_list[0]

    start_input.send_keys('2000/01/01')
    end_input.send_keys(yyyymmdd)

    option_list = driver.find_elements_by_tag_name('option')
    option_value_list = [ option.get_attribute('value') for option in option_list ]
    option_value_list = list(sorted(option_value_list))
    
    assert(fund_code_list==option_value_list)
    
    for option in option_list:

        code = option.get_attribute('value')
        option.click()

        time.sleep(1)

        download_input.send_keys(Keys.RETURN)

        time.sleep(1)

        while not os.path.exists(os.path.join('tmp','fund.csv')):
            time.sleep(0.5)

        time.sleep(1)

        shutil.move(os.path.join('tmp','fund.csv'), os.path.join('output','{}.csv'.format(code)))

        time.sleep(1)

except Exception:
    traceback.print_exc()

if driver is not None:
    driver.close()
