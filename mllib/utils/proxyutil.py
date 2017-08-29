""" Get ZipCodes """
# coding:utf-8

import requests
from mllib.utils import seleniumutil as util
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BSLIB = 'html5lib'
BASE_URL = 'http://www.ip138.com'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
HEADERS = {'user-agent':UA}

iplist = []

def ipvalidate( url, PROXY=None):

    r = None
    if PROXY:
        proxyDict = {'http': "socks5://"+PROXY}
        {'http': "socks5://"+PROXY,
         'https': "socks5://"+PROXY}
        try:
            r = requests.get(url,headers=HEADERS, proxies=proxyDict)
        except requests.exceptions.ConnectionError as e:
            print(PROXY, '无效')
            return
    else:
        r = requests.get(url, headers=HEADERS)
    s = BeautifulSoup(r.text.encode("iso-8859-1").decode("gbk"), BSLIB)

    rows = s.select('body > div.wrapper > div.module.mod-ip > h3')
    if rows:
        print('IP有效: ',url ,rows[0].text)
    else:
        print('')

    ## 待处理问题: 如何处理IFrame


# todo: 将常用免费网站的socks5抓取下来, 并且通过ip38验证
# 争取能将chrome的socks5做成自动获取自动设置; 自动获取容易; 关键是自动设置, 目前只能通过浏览器的扩展
def crawl_socks_url(driver, url):
    print('解析url: ', url)

    driver.get(url)
    print('url解析完毕')
    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.ID, "house-lst"))
    #     )
    # except TimeoutException:
    #     print('加载页面失败')



    ## // Example

    try:
        elements = driver.find_elements_by_xpath('//*[@id="proxylisttable"]/tbody/tr')
        for item in elements:
            ip = util.find_element_by_xpath_text(item, './/td[1]')
            port = util.find_element_by_xpath_text(item, './/td[2]')
            print('ip: ', ip, ' port: ', port)
            iplist.append(ip+':'+port)


    except Exception as e:
        print('程序异常终止!')
        print(e)
    finally:
        pass



if __name__ == '__main__':
    #ipvalidate('http://www.ip138.com/')
    _PROFILE_USE = 'profile1'


    ipvalidate('http://www.ip138.com', '36.66.218.153:1080')

