# database.py

import os
import pymysql
import datetime
import bcrypt

class Database:
    """ Database object to connect to pfmdatabase on AWS """

    def __init__(self):
        host = "pfm-rdbs-instance.cd5ryppsxnnf.ap-northeast-2.rds.amazonaws.com"
        port = 3306
        dbname = 'pfmdatabase'
        user = 'pfmrdbsuser'
        password = os.environ['PFMDBPW']
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
