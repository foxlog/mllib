# coding: utf-8

from selenium import webdriver
import time

from selenium.webdriver import DesiredCapabilities

def create_chrome_driver_OLD(PROXY=None):
    capabilities = dict( DesiredCapabilities.CHROME )

    if not "chromeOptions" in capabilities:
        capabilities['chromeOptions'] = {
            'args' : [],
            'binary' : "",
            'extensions' : [],
            'prefs' : {}
        }

    capabilities['proxy'] = {
        'httpProxy' : "%s" %(PROXY),
        'ftpProxy' : "%s" %(PROXY),
        'sslProxy' : "%s" %(PROXY),
        'noProxy' : None,
        'proxyType' : "MANUAL",
        'class' : "org.openqa.selenium.Proxy",
        'autodetect' : False
    }


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome( chrome_options = options, desired_capabilities=capabilities )
    # 设置等待时间
    #driver.implicitly_wait(5)
    # 最大化窗口
    driver.maximize_window()
    return driver

def create_chrome_driver(PROXY='profile1', NEEDCONFIG=True):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('user-data-dir=/Users/alex/opt/chromedriver-user-data-dir/'+PROXY)

    # 增加 user-data-dir , 用来安装插件

    #不用这种做法, 切换为使用浏览器插件的模式人工设置proxy
    #if PROXY:
    #    options.add_argument('--proxy-server=http://%s' % PROXY)
    driver = webdriver.Chrome(chrome_options = options)
    # 设置等待时间
    #driver.implicitly_wait(5)
    # 最大化窗口
    driver.maximize_window()

    # 打开ip138 测试下代理, 是否有效

    driver.get('http://www.ip138.com/')

    time.sleep(15)

    #print('第一次启动, 3分钟, 用来安装相关插件')
    if NEEDCONFIG:
        time.sleep(60*1)

    return driver

def find_element_by_xpath_selector(item, selector):
    try:
        return item.find_element_by_xpath(selector)
    except:
        return None

def find_elements_by_xpath_selector(item, selector):
    try:
        return item.find_elements_by_xpath(selector)
    except:
        return []


def find_element_by_xpath(item, selector):
    return find_element_by_xpath_selector(item, selector)

def find_element_by_xpath_text(item, selector):
    result = find_element_by_xpath_selector(item, selector)
    if result:
        return result.text
    else:
        return ''

def find_element_by_xpath_attr(item, selector, attr):
    result = find_element_by_xpath_selector(item, selector)
    if result:
        return result.get_attribute(attr)
    else:
        return ''
"""
def wait_time(driver, url, timeout):
    try:
        driver.get(url)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "J_TabBarBox"))
    )
    except TimeoutException:
        return False
    if is_recommends_appear(driver, max_scroll_time):
        print u'已经成功加载出下方橱窗推荐宝贝信息'
        return driver.page_source



js = "window.scrollTo(0,document.body.scrollHeight-" + str(count * count* 200) + ")"
driver.execute_script(js)
1
2
js = "window.scrollTo(0,document.body.scrollHeight-" + str(count * count* 200) + ")"
driver.execute_script(js)
其中 count 是下拉的次数，经过测试之后，每次拉动距离和 count 是平方关系比较科学，具体不再描述，当然你可以改成自己想要的数值。

嗯，加载出来之后，就可以用


driver.page_source
1
driver.page_source
来获取网页源代码了



"""