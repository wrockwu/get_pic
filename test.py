import os
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

global url
url = 'https://www.taobao.com'
global driver
driver = webdriver.Chrome()
global i
i = 0
global k_words
k_words = '比基尼 三点式'
global path_pic
path_pic = '/home/bwu/pics'

def hunter_init():
    logging.info('Start hunter')
    #driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.get(url)

def enter_key_words(words):
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('input#q.search-combobox-input'))
        logging.info('Open URL:%s success'%(url))
    except Exception as e:
        logging.info('error:%s, Open URL:%s failed?'%(e,url))
        driver.close()

    """Page show search bar, wait some seconds
    """
    sleep(random.uniform(1, 2.5))
    elem = driver.find_element_by_name('q')
    elem.clear()
    elem.send_keys(words)

    """Cheat
    """
    sleep(random.uniform(0.5, 1))
    elem.send_keys(Keys.RETURN)

def click_sortbysale_btn():
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('ul.sorts'))
    except Exception as e:
        logging.info('error:%s, Can not get sort bar?'%(e))
        driver.close()
    
    """Cheat
    """
    sleep(random.uniform(1, 2))
    """Change page sort by sale
    """
    elem = driver.find_element_by_link_text('销量')
    actions = ActionChains(driver)
    actions.move_to_element(elem)
    actions.click()
    actions.perform() 

    """Wait page change to sort by sale
    """
    while not (driver.find_element_by_css_selector('a.J_Ajax.link.active').text == '销量从高到低'): 
        sleep(1) 

    logging.info('Change sort mode success')

def click_showbylist_btn():
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.styles'))
    except Exception as e:
        logging.info('error:%s, Can not get list styles bar?'%(e))
        driver.close()
    """Cheat
    """
    sleep(random.uniform(1, 3))
    """Change page to list mode, find the element first
    """
    elems = driver.find_elements_by_css_selector('a.J_Ajax.J_SortbarStyle.link.icon-tag')
    for e in elems:
        if (e.get_attribute('title')) == '列表模式':
            logging.info('find list styles bar')
            break
    ActionChains(driver).move_to_element(e).click().perform()

    """Wait page change to list mode, but we must re-get the elems!!!
       Below code is ugly, but we realy need them!!!
    """
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.list'))
    except Exception as e:
        logging.info('error:%s, Can not change to  list mode?'%(e))
        driver.close()

    logging.info('Change list mode success')

def get_allcomment_elements():
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.list'))
    except Exception as e:
        logging.info('error:%s, Can not get item list?'%(e))
        driver.close()
    """Get all comment link, store in a list
    """
    elems = driver.find_elements_by_class_name('comment')
    logging.info('get item comments list success')

    return elems

def is_tmall_page():
    try:
        curl = driver.current_url
    except Exception as e:
        logging.error('error:%s, Can not get current url'%(e))

    return curl.find('detail.tmall.com') != -1

def click_next_comment_page():
    sleep(random.uniform(5, 8))
    logging.info('click next page button')
    try:
        if is_tmall_page():
            elem = driver.find_element_by_xpath('//a[contains(text(), "下一页")]')
            """current page is last page
            """
            if elem.get_attribute('class') == 'rate-page-next':
                logging.info('reached the last comment page')
                return False
        else:
            elem = driver.find_element_by_xpath('//li[contains(text(), "下一页")]')
            """current page is last page
            """
            if elem.get_attribute('class') == 'pg-next pg-disabled':
                logging.info('reached the last comment page')
                return False
 
        ActionChains(driver).move_to_element(elem).click().perform()
        return True
    except Exception as e:
        logging.error('error:%s, end page?'%(e))
        return False

def click_review_picbtn():
    try:
        if is_tmall_page():
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.rate-toolbar'))
        else:
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.kg-rate-wd-filter-bar'))
        logging.info('Open detail comment success')
    except Exception as e:
        logging.error('error:%s, Open detail comment faild?'%(e))
        return False

    """wait to load full page & Cheat
    """
    sleep(random.uniform(2,3))
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

def get_allpages_picurl():
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

        urls = get_perpage_picurl()
        if urls:
            pages_urls.extend(urls)
        
        """slow down to click next page btn
        """
        if click_next_comment_page():
            continue
        else:
            logging.info('end of comment page')
            break
    
    """remove repetition url
    """
    return set(pages_urls)

def get_perpage_picurl():
    page_urls = []

    try:
        if is_tmall_page():
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.tm-rate-content'))
        else:
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('div.review-details'))
        """Wait page stable
        """
        sleep(1)
        elems = driver.find_elements_by_xpath('//img[contains(@src,"_40x40.jpg")]')
        logging.info('find img url')
    except Exception as e:
        logging.error('error:%s, can not find img url?'%(e))
        return False

    for e in elems:
        url = e.get_attribute('src')[0:-10]
        page_urls.append(url)

    return page_urls

def save_pic(urls):
    global i
    count = 1
    for url in urls:
        req = urllib.request.Request(url=url, headers=headers)
        try:
            data = urllib.request.urlopen(req).read()
        except Exception as e:
            logging.error('error:%s, missing pic url:%s?'%(e, url))
            continue
        f = open(str(i) + '.jpg', 'wb')
        f.write(data)
        logging.info('saved the %d pic, url:%s'%(count, url))
        f.close()
        i += 1
        count += 1
        sleep(random.uniform(1,3))


def download_comment_pic():
    if click_review_picbtn():
        urls = get_allpages_picurl()
        logging.info('total pics:%d'%(len(urls)))
        if urls:
            save_pic(urls)

def create_item_folder():
    try:
        if is_tmall_page():
            elem = driver.find_element_by_xpath('//div[@class="tb-detail-hd"]/h1')
        else:
            elem = driver.find_element_by_xpath('//h3[@class="tb-main-title"]')
    except Exception as e:
        logging.error("error:%s, Can not get item title?"%(e))

#    os.mkdir(path_pic + e.text)

if __name__ == "__main__":

    hunter_init()
    enter_key_words(k_words)
    click_sortbysale_btn()
    click_showbylist_btn()
    elems = get_allcomment_elements()
    for e in elems[1:]:
        sleep(random.uniform(2,3))
        """right click on the comment, to open a new tab
        """
        ActionChains(driver).move_to_element(e).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
    
        """switch to new tab
        """
        handles = driver.window_handles
        print(handles)
        driver.switch_to_window(handles[1])
        
        """Create relate folder
        """
        create_item_folder() 

#        download_comment_pic()
        sleep(random.uniform(3, 6))
    
        """Close the new tab, return to original page
        """
        driver.close()
        driver.switch_to_window(handles[0])
