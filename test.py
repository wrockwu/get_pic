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
import string

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
logging.info('Open URL:%s success'%(url))

elem = driver.find_element_by_name('q')
elem.clear()
elem.send_keys('IPhone')
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
        curl = driver.current_url
    except Exception as e:
        logging.error('error:%s, Can not get current url'%(e))

    return curl.find('detail.tmall.com') != -1

def click_next_comment_page():
    logging.info('click next page button')
    try:
        if is_tmall_page():
            elem = driver.find_element_by_xpath('//a[contains(text(), "下一页")]')
        else:
            elem = driver.find_element_by_xpath('//li[contains(text(), "下一页")]')
 
        ActionChains(driver).move_to_element(elem).click().perform()
        return True
    except Exception as e:
        logging.error('error:%s, end page?'%(e))
        return False

def click_review_pic_btn():
    try:
        if is_tmall_page():
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.rate-toolbar'))
        else:
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.kg-rate-wd-filter-bar'))
        logging.info('Open detail comment success')
    except Exception as e:
        logging.error('error:%s, Open detail comment faild?'%(e))
        return False

    """wait to load full page
    """
    sleep(random.uniform(1,2))
    if is_tmall_page():
        elem = driver.find_element_by_xpath('//label[contains(text(), "图片")]')
    else:
        elem = driver.find_element_by_xpath('//input[@id="reviews-t-val3"]')

    if elem is None:
        logging.info('No pic in commet')
        return False
    else:
        ActionChains(driver).move_to_element(elem).click().perform()
        return True

def get_all_pages_pics_url():
    pages_urls = []

    while True:
        """wait page load full comments
        """
        try:
            if is_tmall_page():
                WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.rate-grid'))
            else:
                WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.tb-revbd'))
            logging.info('show comment success')
        except Exception as e:
            logging.error('error:%s can not show comment?'%(e))
            return False

        pages_urls.extend(get_onepage_pics_url())
        
        """slow down to click next page btn
        """
        sleep(random.uniform(1,5))

        if click_next_comment_page():
            continue
        else:
            logging.info('end of comment page')
            break

    
    """remove repetition url
    """
    return set(pages_urls)

def get_onepage_pics_url():
    page_urls = []

    try:
        if is_tmall_page():
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.tm-rate-content'))
        else:
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.review-details'))

        elems = driver.find_elements_by_xpath('//img[contains(@src,"_40x40.jpg")]')
        logging.info('find img url')
    except Exception as e:
        logging.error('error:%s, can not find img url?'%(e))

    for e in elems:
        url = e.get_attribute('src')[0:-10]
        page_urls.append(url)

    return page_urls

def save_pics(urls):
    global i
    for url in urls:
        req = urllib.request.Request(url=url, headers=headers)
        try:
            data = urllib.request.urlopen(req).read()
        except Exception as e:
            logging.error('error:%s, missing pic url:%s?'%(e, url))
            continue
        f = open(str(i) + '.jpg', 'wb')
        f.write(data)
        logging.info('saved pic, url:%s'%(url))
        f.close()
        i += 1
        sleep(random.uniform(1,3))


def download_comment_pic():
    if click_review_pic_btn():
        urls = get_all_pages_pics_url()
#        if not urls:
#            save_pics(urls)

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
