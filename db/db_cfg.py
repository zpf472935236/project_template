# -*-coding:utf-8-*-

# @Author: 赵朋飞 <pengfeizhao036@gmail.com>
# @Date:   2018-11-16

mysql_host = {
    # 本地数据库
    "desktop": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "",
    },
    # 129 本地连接
    "local": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "shiye",
    },
    "remote": {
        "host":"172.17.23.128",
        "user":"",
        "password":"",
        "port":3306,
    },
    "remote_129": {
        "host":"",
        "user":"",
        "password":"",
        "port":3306,
    },

}

mongo_host = {

}

redis_host = {
    # 本地数据库
    "desktop": {
        "host": "localhost",
        "port": 6379,
        # "user": "root",
        "password": "",
        "db_select": "11",
        "decode_responses": "True",
        "max_memory": "5120",
        "max_connections": "1",

    },
    # 129 本地连接
    "local": {
        "host": "192.168.1.129",
        "port": 6379,
        # "user": "root",
        "password": "shiye",
        "db_select": "11",
        "decode_responses": "True",
        "max_memory": "5120",
        "max_connections": "1",

}
