import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '\x1c\x83u\x15\x04\x8bgq\xde\xa4\x87S\xcf\xb2\xb4\xe7#\xda\x13[^\xe2\x8aV'
DEBUG = True
HOST = '0.0.0.0'
STORAGE_FOLDER = '/opt/wgcna/'
REDIS_DB_SESSION = 0
REDIS_DB_DATA = 1
SESSION_TYPE = 'redis'
SESSION_USE_SIGNER = True