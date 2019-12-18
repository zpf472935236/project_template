# -*-coding:utf-8-*-

# @Author: 赵朋飞 <pengfeizhao036@gmail.com>
# @Date:   2018-11-16

import datetime
import os
import re
import sys
import time
import copy
import uuid
from log_util import logger


is_py3 = sys.version_info.major == 3
if is_py3:
    string_types = (str, bytes)
else:
    string_types = (basestring, )


def text_to_str(text, encoding='utf8'):
    '''
    将传入文本转换为str类型 兼容py2 py3
    '''
    if is_py3:
        if isinstance(text, bytes):
            text = text.decode(encoding)
    else:
        if isinstance(text, unicode):
            text = text.encode(encoding)
    return text

def TimeDeltaYears(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now()
    try:
        return from_date.replace(year=from_date.year + years)
    except:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year + years)


def local_datetime(data):
    '''
    把data转换为日期时间，时区为东八区北京时间，能够识别：今天、昨天、5分钟前等等，如果不能成功识别，则返回datetime.datetime.now()
    '''
    dt = datetime.datetime.now()
    # html实体字符转义
    # data = HTMLParser.HTMLParser().unescape(data)
    data = data.strip()
    if not data:
        return dt
    try:
        data = text_to_str(data)
    except Exception as e:
        logger.error("utc_datetime() error: data is not utf8 or unicode : %s" % data)

    # 归一化
    data = data.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
    data = re.sub("\s+", " ", data)

    year = dt.year

    regex_format_list = [
        # 2013年8月15日 22:46:21
        ("(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", ""),

        # "2013年8月15日 22:46"
        ("(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", ""),

        # "2014年5月11日"
        ("(\d{4}-\d{1,2}-\d{1,2})", "%Y-%m-%d", ""),

        # "2014年5月"
        ("(\d{4}-\d{1,2})", "%Y-%m", ""),

        # "13年8月15日 22:46:21",
        ("(\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", "%y-%m-%d %H:%M:%S", ""),

        # "13年8月15日 22:46",
        ("(\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", "%y-%m-%d %H:%M", ""),

        # "8月15日 22:46:21",
        ("(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "+year"),

        # "8月15日 22:46",
        ("(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "+year"),

        # "8月15日",
        ("(\d{1,2}-\d{1,2})", "%Y-%m-%d", "+year"),

        # "3 秒前",
        ("(\d+)\s*秒前", "", "-seconds"),

        # "3 分钟前",
        ("(\d+)\s*分钟前", "", "-minutes"),

        # "3 秒前",
        ("(\d+)\s*小时前", "", "-hours"),

        # "3 秒前",
        ("(\d+)\s*天前", "", "-days"),

        # 今天 15:42:21
        ("今天\s*(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "date-0"),

        # 昨天 15:42:21
        ("昨天\s*(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "date-1"),

        # 前天 15:42:21
        ("前天\s*(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "date-2"),

        # 今天 15:42
        ("今天\s*(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "date-0"),

        # 昨天 15:42
        ("昨天\s*(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "date-1"),

        # 前天 15:42
        ("前天\s*(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "date-2"),
        # 前天
    ]

    for regex, dt_format, flag in regex_format_list:
        m = re.search(regex, data)
        if m:

            if not flag:
                dt = datetime.datetime.strptime(m.group(1), dt_format)
            elif flag == "+year":
                # 需要增加年份
                dt = datetime.datetime.strptime("%s-%s" % (year, m.group(1)), dt_format)
            elif flag in ("-seconds", "-minutes", "-hours", "-days"):
                flag = flag.strip("-")
                if flag == 'seconds':
                    dt = dt - datetime.timedelta(seconds = int(m.group(1)))
                elif flag=='minutes':
                    dt = dt - datetime.timedelta(minutes=int(m.group(1)))
                elif flag =="hours":
                    dt = dt - datetime.timedelta(hours=int(m.group(1)))
                elif flag=='days':
                    dt = dt - datetime.timedelta(days=int(m.group(1)))
                # exec("dt = dt - datetime.timedelta(%s = int(m.group(1)))" % flag)
            elif flag.startswith("date"):
                del_days = int(flag.split('-')[1])
                _date = dt.date() - datetime.timedelta(days=del_days)
                _date = _date.strftime("%Y-%m-%d")
                dt = datetime.datetime.strptime("%s %s" % (_date, m.group(1)), dt_format)
            return dt
    else:
        logger.error("unknow datetime format: %s" % data)

    return dt


def utc_datetime(data):
    """
    将时间转化为国际时区 datetime类型
    :param data:
    :return:
    """
    try:
        utc_dt = local_datetime(data) - datetime.timedelta(hours=8)
    except Exception as e:
        utc_dt = datetime.datetime.utcnow()
        logger.exception(e)
    return utc_dt


def timestamp_to_date(timestamp, str_format="%Y-%m-%d"):
    """
    将时间戳转化为格式化字符串
    :param timestamp: 时间戳
    :param str_format: 转化时间的格式， 默认 2019-5-5
    :return:
    """
    if len(str(timestamp)) == 13:
        timestamp = int(timestamp) / 1000
    timestamp = float(timestamp)
    time_array = time.localtime(timestamp)
    date_str = time.strftime(str_format, time_array)
    return datetime.datetime.strptime(date_str, str_format)


def local_timestamp(data):
    dt = local_datetime(data)

    tmp = int(time.mktime(dt.timetuple()))
    return tmp


def utc_timestamp(data):
    dt = utc_datetime(data)
    tmp = int(time.mktime(dt.timetuple()))
    return tmp

def now_time_str(str_format="%Y-%m-%d"):
    dt = datetime.datetime.now()
    tr = dt.strftime(str_format)

    return tr


def add_uuid(data):
    """
    对字符串进行加密
    :return:
    """
    data = uuid.uuid3(uuid.NAMESPACE_DNS, data)
    data = str(data)
    result_data = data.replace('-', '')
    return result_data



if __name__ == '__main__':
    a = local_timestamp('aasfasdfa%Y-%m-%d %H:%M:%S')
    # b = local_timestamp('今天')
    # c = timestamp_to_date(a, '%Y-%m-%d %H:%M:%S')
    # # d = timestamp_to_date(b, '%Y-%m-%d %H:%M:%S')
    # print(b)
    # print(c, type(c))
    # d = now_time_str("%Y%m%d")
    print(a)
