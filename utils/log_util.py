# encoding=utf-8

# @Author: 赵朋飞 <pengfeizhao036@gmail.com>
# @Date:   2018-11-16

import logging
import logging.handlers
import time
import os,sys


# log_path是存放日志的路径
cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'logs/%s'%time.strftime('%Y_%m_%d'))
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path): os.mkdir(log_path)

def get_log_file_name(path):
    file_name = os.path.basename(path)
    log_file_name = file_name.split('.')[0] + '.log'
    return log_file_name

logger = logging.getLogger()
log_file_name = get_log_file_name(sys.argv[0])
logname = os.path.join(log_path, log_file_name)
# 本地日志文件
fp = logging.FileHandler(logname, mode='a', encoding='utf-8')
logger.addHandler(fp)

# 标准输出流
std = logging.StreamHandler(sys.stdout)
logger.addHandler(std)

# 定制标准输出和本地文件日志格式
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s] [%(lineno)d] - %(message)s")
fp.setFormatter(formatter)
std.setFormatter(formatter)

logger.setLevel(logging.NOTSET)
logger.setLevel(logging.NOTSET)

if __name__ == '__main__':
    logger.debug("I'm spider man")
