import os
import sqlite3

filepath = os.environ.get('CM_FILEPATH', 'CableInfo.txt')
sqlite_db = os.environ.get('CM_SQLITE_DB', 'cable_modem.db')
db_file = os.environ.get('DB_FILE', 'cable_modem.db')

def sqlconn():
    return sqlite3.connect(db_file, check_same_thread=False)

def cable_info_file():
    return open(filepath, 'r')