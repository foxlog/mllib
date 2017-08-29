# -*- coding: utf-8 -*-


"""
时间日期 转换函数

"""
from datetime import date, timedelta, datetime

def date_to_ymd_str(dates):

    return dates.strftime('%Y-%m-%d')

def str_to_date(strs):
    return datetime.strptime(strs, '%Y-%m-%d')

def get_yesterday_str():
    yesterday = date.today() - timedelta(1)
    return yesterday.strftime('%Y-%m-%d')


def get_yesterday_date():
    yesterday = date.today() - timedelta(1)
    return yesterday

def get_backdays_date(intDays):
    to_back_day = date.today() - timedelta(intDays)
    return to_back_day

def get_backdays_str(intDays):
    to_back_day = date.today() - timedelta(intDays)
    return to_back_day.strftime('%Y-%m-%d')

def get_today_date():
    return date.today()

def get_today_str():
    return date.today().strftime('%Y-%m-%d')
