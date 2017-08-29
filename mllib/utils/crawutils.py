# -*- coding: utf-8 -*-

"""
爬虫抓取工具

"""

import numpy as np
import time
import uuid
import sys
from mllib.utils import seleniumutil as util
import re
import lxml.html
import pandas as pd
from lxml import etree
from urllib.request import urlopen, Request
import requests
from pandas.compat import StringIO
from mllib.utils import config_vars as CONFIG
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait




# 嵌套查询, 针对那些嵌套的 html 一次取出所有 text, 返回一个大的字符串
from selenium.common.exceptions import WebDriverException

def scroll_mouse(driver):
    try:
        js1 = "window.scrollTo(0,250)"
        js2 = "window.scrollTo(250,0)"
        js3 = "window.scrollTo(0,document.body.scrollHeight)"
        js_window_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script(js1)
        time.sleep(1)
        driver.execute_script(js2)
        time.sleep(1)
        driver.execute_script(js3)
        time.sleep(1)
    except WebDriverException:
        print('页面下拉失败')

def get_all_children_elements_chrome(element):
    result = ''
    all_infos = util.find_element_by_xpath(element, './descendant-or-self::node()/text()')
    for s in all_infos:
        #print('type(s)', type(s))
        #print('s', s)
        result = result + ' ' + s.strip()
        #print('result: ', result)



    return result

def get_all_children_elements(element):
    result = ''
    all_infos = element[0].xpath('./descendant-or-self::node()/text()')
    for s in all_infos:
        #print('type(s)', type(s))
        #print('s', s)
        result = result + ' ' + s.strip()
        #print('result: ', result)



    return result


# 新浪财经数据
def get_sina_finance_data(retry_count = 3, pause = 0.01, dataArr=pd.DataFrame(), pageNo=1, endPage=3):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(CONFIG.SINA_URL%(pageNo), headers=CONFIG.HEADERS)
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id=\"dataTable\"]/tr")

            sarr = [etree.tostring(node).decode('utf-8') for node in res]

            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df.columns = CONFIG.SINA_COLUMNS
            dataArr = dataArr.append(df, ignore_index=True)
            #a[last()]/@onclick
            nextPage = html.xpath('//div[@class=\"pages\"]/a[last()]/@onclick')
            if len(nextPage)>0 and int(pageNo) < endPage:
                pageNo = re.findall(r'\d+', nextPage[0])[0]
                return get_sina_finance_data(retry_count, pause, dataArr, pageNo=pageNo)
            else:
                return dataArr
        except Exception as e:
            print(e)

# 链家网数据
def get_lianjia_rent_data(retry_count = 3, pause = 0.01, dataArr=[], pageNo=1, endPage=3):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request_1 = Request(CONFIG.LIANJIA_URL%(pageNo))
            text_1 = urlopen(request_1, timeout=10).read()
            text_1 = text_1.decode('utf-8')
            html_1 = lxml.html.parse(StringIO(text_1))
            res_1 = html_1.xpath("//*[@id=\"house-lst\"]/li/div[@class=\"info-panel\"]")
            links_1 = html_1.xpath("//*[@id=\"house-lst\"]/li/div[@class=\"info-panel\"]/h2/a/@href")

            for link in links_1:
                request_2 = Request(link)
                text_2 = urlopen(request_2, timeout=10).read()
                text_2 = text_2.decode('utf-8')
                html_2 = lxml.html.parse(StringIO(text_2))
                _price = html_2.xpath("//div[@class=\"price \"]/span[@class=\"total\"]/text()")
                _area = html_2.xpath("//div[@class=\"zf-room\"]/p[1]/text()")
                _house_type = html_2.xpath("//div[@class=\"zf-room\"]/p[2]/text()")
                _stair_level=html_2.xpath("//div[@class=\"zf-room\"]/p[3]/text()")
                _house_direction=html_2.xpath("//div[@class=\"zf-room\"]/p[4]/text()")
                _subway = html_2.xpath("//div[@class=\"zf-room\"]/p[5]/text()")
                _xiaoqu_1 = html_2.xpath("//div[@class=\"zf-room\"]/p[6]/a[1]/text()")
                _xiaoqu_2 = html_2.xpath("//div[@class=\"zf-room\"]/p[6]/a[2]/text()")
                _house_num = html_2.xpath("//div[@class=\"houseRecord\"]/span/text()")
                #_other_all = html_2.xpath("//div[@class=\"content zf-content\"]/descendant::*/text()")

                _tmp  = []
                _tmp.append(_price)
                _tmp.append(_area)
                _tmp.append(_house_type)
                _tmp.append(_stair_level)
                _tmp.append(_house_direction)
                _tmp.append(_subway)
                _tmp.append('-'.join(_xiaoqu_1 + _xiaoqu_2) )
                _tmp.append(_house_num)
                #_tmp.append(_other_all[0].strip())

                print(_tmp)
                dataArr.append(_tmp)




            nextPage = html_1.xpath('//a[text()=\'下一页\']/@href')
            if len(nextPage)>0 and int(pageNo) < endPage:
                #pageNo = re.findall(r'\d+', nextPage[0])[0]
                nextPage = 'https://bj.lianjia.com' + nextPage
                return get_lianjia_rent_data(retry_count, pause, dataArr, pageNo=pageNo)
            else:
                return dataArr
        except Exception as e:
            print(e)



# 链家网数据
def craw_lianjia_rent_data_sandbox(retry_count = 3, pause = 1, dataArr=[],pageNo='/zufang/pg1', endPage=3):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
            HEADERS = {'user-agent': UA}

            COOKIES="select_city=110000; all-lj=eae2e4b99b3cdec6662e8d55df89179a; lianjia_uuid=27657801-7728-4cdd-a8a6-2c91da633c92; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _smt_uid=59a4cafa.20fe3268; _ga=GA1.2.402296747.1503972092; _gid=GA1.2.1448219226.1503972092; lianjia_ssid=242c6dac-12ad-49db-a047-9a32f0e6ff44"
            COOKIES = dict(x.split('=') for x in COOKIES.split(';'))
            print('cookie: ',  COOKIES)
            #request_1 = Request(CONFIG.LIANJIA_URL%(pageNo), headers=HEADERS)
            request_1 = requests.get(CONFIG.LIANJIA_URL%(pageNo), headers=HEADERS, cookies=COOKIES)
            #text_1 = urlopen(request_1, timeout=10).read()
            text_1 = request_1.text
            #print('text: ', text_1)
            #text_1 = text_1.decode('utf-8')

            #print('text: ', text_1)
            html_1 = lxml.html.parse(StringIO(text_1))
            res_1 = html_1.xpath("//*[@id=\"house-lst\"]/li/div[@class=\"info-panel\"]")
            #links_1 = html_1.xpath("//*[@id=\"house-lst\"]/li/div[@class=\"info-panel\"]/h2/a/@href")
            _tmp = []

            for res in res_1:


                link = res.xpath(".//h2/a/@href") # detail 连接

                _where = res.xpath(".//div[@class=\"where\"]")
                _other = res.xpath(".//div[@class=\"other\"]")
                _chanquan = res.xpath(".//div[@class=\"chanquan\"]")

                # 获取所有
                _whereResult = get_all_children_elements(_where)
                _otherResult = get_all_children_elements(_other)
                _chanquanResult = get_all_children_elements(_chanquan)

                #request_2 = Request(link[0])
                request_2 = requests.get(link[0], headers=HEADERS, cookies=COOKIES)
                #text_2 = urlopen(request_2, timeout=10).read()
                text_2 = request_2.text
                #text_2 = text_2.decode('utf-8')
                html_2 = lxml.html.parse(StringIO(text_2))
                _price = html_2.xpath("//div[@class=\"price \"]/span[@class=\"total\"]/text()")
                _area = html_2.xpath("//div[@class=\"zf-room\"]/p[1]/text()")
                _house_type = html_2.xpath("//div[@class=\"zf-room\"]/p[2]/text()")
                _stair_level=html_2.xpath("//div[@class=\"zf-room\"]/p[3]/text()")
                _house_direction=html_2.xpath("//div[@class=\"zf-room\"]/p[4]/text()")
                _subway = html_2.xpath("//div[@class=\"zf-room\"]/p[5]/text()")
                _xiaoqu_1 = html_2.xpath("//div[@class=\"zf-room\"]/p[6]/a[1]/text()")
                _xiaoqu_2 = html_2.xpath("//div[@class=\"zf-room\"]/p[6]/a[2]/text()")
                _house_num = html_2.xpath("//div[@class=\"houseRecord\"]/span/text()")

                _tmp.append(_whereResult)
                _tmp.append(_otherResult)
                _tmp.append(_chanquanResult)
                _tmp.append(_price[0].strip())
                _tmp.append(_area[0].strip())
                _tmp.append(_house_type[0].strip())
                _tmp.append(_stair_level[0].strip())
                _tmp.append(_house_direction[0].strip())
                _tmp.append(_subway[0].strip())
                _tmp.append('-'.join(_xiaoqu_1 + _xiaoqu_2) )
                _tmp.append(_house_num[0].strip())

                print(_tmp)
                dataArr.append(_tmp)

                _tmp = []

            nextPage_Char = u'下一页'
            nextPage = html_1.xpath("//a[text()=\"%s\"]/@href" %(nextPage_Char))
            #nextPage = html_1.xpath('//a[text()=\'下一页\']/@href')
            print('nextPage:', ''.join(nextPage))
            if len(nextPage)>0 :
                #pageNo = re.findall(r'\d+', nextPage[0])[0]
                #nextPage = 'https://bj.lianjia.com' + nextPage
                return craw_lianjia_rent_data_sandbox(retry_count, pause, dataArr, pageNo=''.join(nextPage))
            else:
                return dataArr
        except Exception as e:
            print(e)



# 通过 chrome 下载数据
def craw_lianjia_chrome(driver, url, target_page):
    random_seconds = random.randint(2, 6)
    time.sleep(random_seconds)
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "house-lst"))
        )
    except TimeoutException:
        print('加载页面失败')

    scroll_mouse(driver)


    try:
        elements = driver.find_elements_by_xpath('//*[@id="house-lst"]/li')
        for item in elements:
            # print(item.get_attribute('innerHTML'))

            UUID = str(uuid.uuid4())  ## 统一编号

            detail_page_url = util.find_element_by_xpath_attr(item, './/div/h2/a', "href")
            print('detail page url: ', detail_page_url)
            page_info = target_page  # 记录到csv里作为以后定位异常
            title = util.find_element_by_xpath_text(item, './/div/h2/a')
            region = util.find_element_by_xpath_text(item, './/div/div/div/a/span')
            zone = util.find_element_by_xpath_text(item, './/div/div/div/span/span')
            meters = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[1]/span[2]')
            direction = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[1]/span[3]')
            others = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[2]')
            subway = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[3]/div/div/span[2]/span')
            kanfang = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[3]/div/div/span[4]/span')
            decoration = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[3]/div/div/span[6]/span')
            heating = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[3]/div/div/span[8]/span')
            price = util.find_element_by_xpath_text(item, './/div[2]/div[2]/div[1]/span')
            updated_time = util.find_element_by_xpath_text(item, './/div[2]/div[2]/div[2]')
            view_num = util.find_element_by_xpath_text(item, './/div[@class="square"]/div/span[@class="num"]')



            _where = util.find_element_by_xpath(item, './/div[@class="where"]')
            # 获取所有
            # selenium和lxml里的 xpath 显示所有直接点不一样, selenium 直接 text 就可以全部显示
            print('where: ', ' '.join(_where.text.strip().splitlines()))

            _other = util.find_element_by_xpath(item, './/div[@class="other"]')
            print('other: ', ' '.join(_other.text.strip().splitlines()))

            _chanquan = util.find_element_by_xpath(item, './/div[@class="chanquan"]')
            print('chanquan: ', ' '.join(_chanquan.text.strip().splitlines()))

            # 新增extra_info
            #extra_info = util.find_element_by_xpath_text(item, './/div[2]/div[1]/div[3]/div/div')

            df = pd.DataFrame(data=[
                [UUID, detail_page_url, page_info, title, region, zone, meters, direction, others, subway, kanfang,
                 decoration, heating, price, updated_time, view_num, _where, _other, _chanquan]])
            df.to_csv('/Users/alex/tmp/lianjiaindex500.csv', mode='a', header=False, encoding='gb18030', index=False)
            df2 = pd.DataFrame(data=[[UUID, detail_page_url]])
            df2.to_csv('/Users/alex/tmp/lianjiadetailurl500.csv', mode='a', header=False, encoding='gb18030',
                       index=False)
    except Exception as e:
        print('异常时的target_page:', target_page)  # return products
        print(e)
        sys.exit(0)
    finally:
        pass


def _lianjia_chrome_demo():
    index_flag = 1
    driver = util.create_chrome_driver(NEEDCONFIG=False)

    # parse(driver, index_page, index_flag)
    # parse_detail(driver, 'https://bj.lianjia.com/zufang/101101773111.html')
    # 先来10页测试下

    nums_to_sleep = 1
    for i in range(0, 500):
        index_page = 'https://bj.lianjia.com/zufang/pg' + str(index_flag)
        # 爬10页休息一次
        if nums_to_sleep == 10:
            _big_sleep = random.randint(10, 20)
            print("来一次大的休息: ", _big_sleep)
            time.sleep(_big_sleep)
            nums_to_sleep = 1
        craw_lianjia_chrome(driver, index_page, index_flag)
        index_flag += 1
        nums_to_sleep += 1

    # parse_summary_page(index_page)
    # parse_by_bs('https://bj.lianjia.com/zufang/pg1')

    driver.quit()

if __name__ == '__main__':
    #result = get_lianjia_rent_data_sandbox(endPage=10)

    #print('size: ', len(result))
    _lianjia_chrome_demo()