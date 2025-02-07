import os
import sqlite3

CM_FILEPATH = os.environ.get('CM_FILEPATH', 'CableInfo.txt')
CM_SQLITE_DB = os.environ.get('CM_SQLITE_DB', 'cable_modem.db')
MODEM_PW = os.environ.get('MODEM_PW')

assert MODEM_PW, "MODEM_PW environment variable not set"

def sqlconn():
    return sqlite3.connect(CM_SQLITE_DB, check_same_thread=False)

def cable_info_file():
    return open(CM_FILEPATH, 'r')