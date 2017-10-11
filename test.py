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
import urllib
import random

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

headers = {
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/61.0.3163.100 Safari/537.36',      
        
}

cate_list = []
url = 'https://www.taobao.com'

i = 0

logging.info('Start hunter')
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver = webdriver.Chrome()
driver.get(url)
sleep(1)
try:
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'q')))
except:
    driver.close()
logging.info('Open URL success')

elem = driver.find_element_by_name('q')
elem.clear()
elem.send_keys('好奇小姐')
elem.send_keys(Keys.RETURN)
sleep(2)

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

def is_tmall_page():
    try:
        elem = driver.find_element_by_id('mallLogo')
    except Exception as e:
        elem = None
#        print('erro:%s'%(e))

    if elem is None:
        return False
    else:
        return True

def click_pic_review_btn():
    if is_tmall_page():
        elem = driver.find_element_by_xpath('//label[contains(text(), "图片")]')
    else:
        elem = driver.find_element_by_xpath('//input[@id="reviews-t-val3"]')

    if elem is None:
        logging.info('No pic in commet')
    else:
        ActionChains(driver).move_to_element(elem).click().perform()

def get_pics_url():
    urls = []
    elems = driver.find_elements_by_xpath('//img[contains(@src,"0-rate.jpg_40x40.jpg")]')
    logging.info('img url:%s'%(elems))
    for e in elems:
        url = e.get_attribute('src')[0:-10]
        urls.append(url)

    return urls

def save_pics(urls):
    global i
    for url in urls:
        req = urllib.request.Request(url=url, headers=headers)
        try:
            data = urllib.request.urlopen(req).read()
        except Exception as e:
            print('missing pic')
            continue
        f = open(str(i) + '.jpg', 'wb')
        f.write(data)
        print ("正在保存的一张图片为")
        f.close()
        i += 1
        s_time= random.uniform(1,3)
        print(s_time)
        sleep(random.uniform(1,3))


def download_comment_pic():
    click_pic_review_btn()
    """Wait page load full comment with pic
    """
    sleep(random.uniform(3,5))
    urls = get_pics_url()

    save_pics(urls)

for e in elems:
    sleep(random.uniform(2,4))
    logging.info(e.get_attribute('href'))
    """right click on the comment, to open a new tab
    """
    ActionChains(driver).move_to_element(e).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    """switch to new tab
    """
    handles = driver.window_handles
    logging.info(handles)
    logging.info(driver.current_window_handle)
    driver.switch_to_window(handles[1])
    logging.info(driver.current_window_handle)
    
    """wait for load full comment page
    """
    sleep(random.uniform(3,5))    
    download_comment_pic()
    sleep(random.uniform(3,5))


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
