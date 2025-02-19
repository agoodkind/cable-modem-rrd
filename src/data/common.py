import os

CM_FILEPATH = os.environ.get('CM_FILEPATH', 'CableInfo.txt')

MODEM_PW = os.environ.get('MODEM_PW')
assert MODEM_PW, "MODEM_PW environment variable not set"

MODEM_HOST= os.environ.get("MODEM_HOST", "192.168.100.1")
LOG_FILE = os.environ.get('LOG_FILE', 'cable_modem.log')

PG_PASSWORD = os.environ.get('PG_PASSWORD')
assert PG_PASSWORD, "PG_PASSWORD environment variable not set"

PG_USER = os.environ.get('PG_USER')
assert PG_USER, "PG_USER environment variable not set"

PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_PORT = os.environ.get('PG_PORT', '5432')
PG_DB = os.environ.get('PG_DB', 'cm_data')
