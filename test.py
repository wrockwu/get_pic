from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

cate_list = []
url = 'http://www.taobao.com'
driver = webdriver.Chrome()
#driver.get(url)
#try:
#    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'q')))
#except:
#    driver.close()
#
#elem = driver.find_element_by_name('q')
#elem.clear()
#elem.send_keys('比基尼')
#elem.send_keys(Keys.RETURN)
#
#"""Change page sort by sale
#"""
#menue = driver.find_element_by_link_text('销量')
#actions = ActionChains(driver)
#actions.move_to_element(menue)
#actions.click()
#actions.perform()
#
#"""Wait page change to sort by sale
#"""
#while not (driver.find_element_by_css_selector('a.J_Ajax.link.active').text == '销量从高到低'):
#    sleep(1)
#
#"""Change page to list mode, find the element first
#"""
#elems = driver.find_elements_by_css_selector('a.J_Ajax.J_SortbarStyle.link.icon-tag')
#for e in elems:
#    if (e.get_attribute('title')) == '列表模式':
#        break
#ActionChains(driver).move_to_element(e).click().perform()
#
#"""Wait page change to list mode
#"""
#while not (e.get_attribute('class') == 'J_Ajax J_SortbarStyle link icon-tag active icon-hover'):
#    sleep(1)
#    elems = driver.find_elements_by_css_selector('a.J_Ajax.J_SortbarStyle.link.icon-tag')
#    for e in elems:
#        if (e.get_attribute('title')) == '列表模式':
#            break
#
#"""Get all comment link, store in a list
#"""
#elems = driver.find_elements_by_class_name('comment')
#for e in elems:
#   print(e.get_attribute('href'))
#


driver.get('https://item.taobao.com/item.htm?spm=a230r.1.14.9.6b47abc9C226eH&id=533113514597&ns=1&abbucket=15&on_comment=1')
sleep(20)
#try:
#    WebDriverWait(driver, 20).until(lambda x: x.find_element_by_link_text('图片'))
#except:
#    driver.close()
elem = driver.find_element_by_link_text('图片')
ActionChains.move_to_element(elem).click().perform()
