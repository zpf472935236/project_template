import os, sys
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_dir)
import pymongo
from db_cfg import mysql_host


class BaseMongoPool(object):
    def __init__(self, host, port, user, password, db_name=None):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None

class MongoPool(BaseMongoPool):
    """
    """
    pass
