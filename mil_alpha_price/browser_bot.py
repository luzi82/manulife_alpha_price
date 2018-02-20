HOME_URL='https://www.manulife.com.hk/wps/portal/pwshome/dfp'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
FirefoxProfile = webdriver.firefox.firefox_profile.FirefoxProfile

profile = FirefoxProfile('profile')
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", '/Users/luzi.leung/project/fund/workspace/manulife_alpha_price/')

driver = webdriver.Firefox(firefox_profile=profile)

driver.get(HOME_URL)

ele_list = driver.find_elements_by_tag_name('a')
ele_list = list(filter(lambda _ele:_ele.text.strip() == 'Alpha', ele_list))
assert(len(ele_list)==1)
ele = ele_list[0]

ele.send_keys(Keys.RETURN)

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

ele.send_keys(Keys.RETURN)

index_url = driver.current_url
print(index_url)

ele_list = driver.find_elements_by_tag_name('tbody')
ele_list = list(filter(lambda _ele: ':mainContent:' in _ele.get_attribute('id'),ele_list))
tbody_list = ele_list

tr_list = []
for tbody in tbody_list:
    tr_list = tr_list + tbody.find_elements_by_tag_name('tr')

fund_key_list = [ tr.find_elements_by_tag_name('td')[0].text for tr in tr_list ]



ele_list = driver.find_elements_by_tag_name('input')
ele_list = list(filter(lambda _ele: 'Download Data' in _ele.get_attribute('value'),ele_list))
assert(len(ele_list)==1)
ele = ele_list[0]

ele.send_keys(Keys.RETURN)

driver.close()
