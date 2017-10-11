import logging
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

dcap=dict(DesiredCapabilities.PHANTOMJS)
dcap['PhantomJS.page.settings.resourceTimeout'] = 1000
#dcap['PhantomJS.page.settings.loadTime'] = True
#dcap['PhantomJS.page.settings.disk-cache'] = True
#dcap['PhantomJS.page.customHeaders.Cookies'] = ''
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (X11; Linux x86_64) \
                                            AppleWebKit/537.36 (KHTML, like Gecko) \
                                            Chrome/61.0.3163.100 Safari/537.36')
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s', \
                    filename='hunter.log', filemode='w')

cate_list = []
url = 'https://www.taobao.com'

logging.info('Start hunter')
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver = webdriver.Chrome()
driver.get(url)
try:
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'q')))
except:
    driver.close()
logging.info('Open URL success')

elem = driver.find_element_by_name('q')
elem.clear()
elem.send_keys('Fisher Price')
elem.send_keys(Keys.RETURN)

"""Change page sort by sale
"""
menue = driver.find_element_by_link_text('销量')
actions = ActionChains(driver)
actions.move_to_element(menue)
actions.click()
actions.perform() 

"""Wait page change to sort by sale
"""
while not (driver.find_element_by_css_selector('a.J_Ajax.link.active').text == '销量从高到低'):
    sleep(1)
logging.info('Change sort mode success')

"""Change page to list mode, find the element first
"""
elems = driver.find_elements_by_css_selector('a.J_Ajax.J_SortbarStyle.link.icon-tag')
for e in elems:
    logging.info(e.text)
    if (e.get_attribute('title')) == '列表模式':
        break
ActionChains(driver).move_to_element(e).click().perform()

"""Wait page change to list mode
"""
while not (e.get_attribute('class') == 'J_Ajax J_SortbarStyle link icon-tag active icon-hover'):
    sleep(1)
    elems = driver.find_elements_by_css_selector('a.J_Ajax.J_SortbarStyle.link.icon-tag')
    for e in elems:
        logging.info(e.get_attribute('title'))
        logging.info(e.get_attribute('calss'))
        if (e.get_attribute('title')) == '列表模式':
            break
logging.info('Change list mode success')

"""Get all comment link, store in a list
"""
#elems = driver.find_elements_by_css_selector('a.comment')
elems = driver.find_elements_by_class_name('comment')

def click_pic_review_btn():
    elem = driver.find_element_by_css_selector('input#reviews-t-val3')
    #elem = driver.find_element_by_css_selector('a.tb-tab-anchor')
    ActionChains(driver).move_to_element(elem).click().perform()

def download_comment_pic():
    click_pic_review_btn()

for e in elems:
    logging.info(e.get_attribute('href'))
    """right click on the comment, to open a new tab
    """
    ActionChains(driver).move_to_element(e).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    """switch to new tab
    """
    handles = driver.window_handles
    print(handles)
    print(driver.current_window_handle)
    driver.switch_to_window(handles[1])
    print(driver.current_window_handle)
    
    """wait for load full comment page
    """
    sleep(10)    
    download_comment_pic()
    sleep(3)

    """Close the new tab, return to original page
    """
    driver.close()
    driver.switch_to_window(handles[0])




#"""right click on the comment, to open a new tab
#"""
#e = elems[0]
#ActionChains(driver).move_to_element(e).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
#
#"""switch to new tab
#"""
#handles = driver.window_handles
#driver.switch_to_window(handles[1])
#sleep(3)
#
#"""Close the new tab
#"""
#driver.close()
#driver.switch_to_window(handles[0])

#driver.get('https://item.taobao.com/item.htm?spm=a230r.1.14.9.6b47abc9C226eH&id=533113514597&ns=1&abbucket=15&on_comment=1')
#sleep(20)
#try:
#    WebDriverWait(driver, 20).until(lambda x: x.find_element_by_link_text('图片'))
#except:
#    driver.close()
#elem = driver.find_element_by_link_text('图片')
#ActionChains.move_to_element(elem).click().perform()
