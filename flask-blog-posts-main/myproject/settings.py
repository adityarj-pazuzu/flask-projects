import os

from dotenv import load_dotenv

load_dotenv()
'''
SECRET_KEY = getenv('SECRET_KEY')
DB_USERNAME = getenv('DB_USERNAME')
DB_PASSWORD = getenv('DB_PASSWORD')
DATABASE_NAME = getenv('DATABASE_NAME')
DB_HOST = getenv('DB_HOST')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+ DB_USERNAME + ':%s'%quote(DB_PASSWORD) + '@' + DB_HOST + '/' + DATABASE_NAME
if DB_USERNAME is None:'''

SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
