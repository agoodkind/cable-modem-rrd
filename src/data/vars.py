import os
import sqlite3

CM_FILEPATH = os.environ.get('CM_FILEPATH', 'CableInfo.txt')
CM_SQLITE_DB = os.environ.get('CM_SQLITE_DB', 'cable_modem.db')
MODEM_PW = os.environ.get('MODEM_PW')
MODEM_HOST= os.environ.get("MODEM_HOST", "192.168.100.1")

assert MODEM_PW, "MODEM_PW environment variable not set"

def sqlconn():
    return sqlite3.connect(CM_SQLITE_DB, check_same_thread=False)

def cable_info_file(write=False):
    if write:
        return open(CM_FILEPATH, 'wb')
    return open(CM_FILEPATH, 'r')