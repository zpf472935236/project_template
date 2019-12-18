### 项目目录模板

```
.
├── conf  # 配置文件目录
│
├── db    # 数据库相关封装
│
├── logs  # 日志文件目录
│
├── main_process  # 主逻辑目录
│
└── utils # 功能函数目录
```

### db

目录中db_cfg.py 保存的是各个数据库的连接信息
```python
# mysql连接信息
mysql_host = {
	
}

# mongodb 连接信息
mongo_host = {

}
# redis 连接信息
redis_host = {

}

```
### utils 
用于日志的模块 log_util.py
各种常用函数模块封装 util.py





