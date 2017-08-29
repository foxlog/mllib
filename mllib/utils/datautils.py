"""

获取通用数据的工具库

"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_boston, load_breast_cancer, load_diabetes

import tushare as ts

import dateutils

import os.path

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))





# 链家网数据
def get_lianjia_data():
    path = os.path.join(CURRENT_PATH, "../data/lj_data.csv")
    return pd.read_csv(path, encoding='gb18030')

# 正太分布数据
def get_normalize_data(size = 1000):
    x = np.random.normal(size)
    y = np.random.normal(size)

    return (x, y)

# 均匀分布
def get_linspace_data(a, b, num=5):
    return np.linspace(a, b, num)

# flower
def get_iris_flower_data():
    return load_iris()

def get_boston_house_price():
    return load_boston()

# 乳谢癌数据
def get_breast_cancer_disease_data():
    return load_breast_cancer()

# 糖尿病数据
def get_diabetes_disease_data():
    return load_diabetes()

# 小费
def get_tips_data():
    path = os.path.join(CURRENT_PATH, "../data/tips.csv")
    return pd.read_csv(path)

# 坦坦尼克号死亡情况数据
def get_titanic_data():
    path = os.path.join(CURRENT_PATH, "../data/titanic.csv")
    return pd.read_csv(path)

# 银行用户信用数据
def get_bank_credit_data():
    path = os.path.join(CURRENT_PATH, "../data/credit-data.csv")
    return pd.read_csv(path)

# 航班用户数据
def get_flights_passengers_data():
    path = os.path.join(CURRENT_PATH, "../data/flights.csv")
    return pd.read_csv(path)

# Google stock data
def get_stocks_google():
    path = os.path.join(CURRENT_PATH, "../data/GOOG.csv")
    return pd.read_csv(path)

# apple stock data
def get_stocks_nvidia():
    path = os.path.join(CURRENT_PATH, "../data/NVDA.csv")
    return pd.read_csv(path)

# msft stock data
def get_stocks_msft():
    path = os.path.join(CURRENT_PATH, "../data/MSFT.csv")
    return pd.read_csv(path)

# apple stock data
def get_stocks_apple():
    path = os.path.join(CURRENT_PATH, "../data/AAPL.csv")
    return pd.read_csv(path)

# 80条最新财经新闻
def get_latest_finance_news():
    return ts.get_latest_news()  # 默认获取最近80条新闻数据，只提供新闻类型、链接和标题

# 实时电影票房数据
def get_realtime_movies_boxoffice():
    return ts.realtime_boxoffice()

# 昨日票房
def get_yesterday_movies_boxoffice():
    return ts.day_boxoffice()

# 上月票房
def get_last_month_movies_boxoffice():
    return ts.month_boxoffice()

# 股票 行业分类
def get_finance_industry_classify():
    return ts.get_industry_classified()

# 股票 概念分类
def get_finance_concept_classify():
    return ts.get_concept_classified()

# 股票龙虎榜数据
def get_finance_top_list():
    lst =  ts.top_list(dateutils.get_today_str())
    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(1))

    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(2))

    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(3))

    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(4))

    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(5))

    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(6))

    if len(lst) == 0:
        lst = ts.top_list(dateutils.get_backdays_str(7))

    return lst


# 营业部上榜数据
def get_finance_broker_top_list():
    return ts.broker_tops()


# yahoo 收盘价s
# see here: http://www.learndatasci.com/python-finance-part-yahoo-finance-api-pandas-matplotlib/
def get_yahoo_finance_close_data(froms='2016-01-01',tos='2017-08-28', tickers=['AAPL', 'MSFT', 'SPY']):
    from pandas_datareader import data

    # Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
    #tickers = ['AAPL', 'MSFT', 'SPY']

    # Define which online source one should use
    data_source = 'google'

    # We would like all available data from 01/01/2000 until 12/31/2016.
    start_date = froms
    end_date = tos

    # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    panel_data = data.DataReader(tickers, data_source, start_date, end_date)

    # Getting just the adjusted closing prices. This will return a Pandas DataFrame
    # The index in this DataFrame is the major index of the panel_data.
    close = panel_data.ix['Close']

    # Getting all weekdays between 01/01/2000 and 12/31/2016
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

    # How do we align the existing prices in adj_close with our new set of dates?
    # All we need to do is reindex close using all_weekdays as the new index
    close = close.reindex(all_weekdays)

    return close

if __name__ == '__main__':
    df = get_lianjia_data()
    print(df)