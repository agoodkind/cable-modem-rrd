import os
import sqlite3

import aiosqlite

CM_FILEPATH = os.environ.get('CM_FILEPATH', 'CableInfo.txt')
CM_SQLITE_DB = os.environ.get('CM_SQLITE_DB', 'cable_modem.db')
MODEM_PW = os.environ.get('MODEM_PW')
MODEM_HOST= os.environ.get("MODEM_HOST", "192.168.100.1")
LOG_FILE = os.environ.get('LOG_FILE', 'cable_modem.log')

assert MODEM_PW, "MODEM_PW environment variable not set"

def sqlconn():
    return sqlite3.connect(CM_SQLITE_DB, check_same_thread=False)


def async_sqlconn():
    """
    Example usage:
    
    async with async_sqlconn() as conn:
        async with conn.execute("SELECT * FROM table") as cursor:
            async for row in cursor:
                print(row)
    """
    return aiosqlite.connect(CM_SQLITE_DB)

def cable_info_file(write=False):
    if write:
        return open(CM_FILEPATH, 'wb')
    return open(CM_FILEPATH, 'r')