import os

DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']
DB_PORT = os.environ['DATABASE_PORT']

REDIS_HOST = os.environ['REDIS_HOST']

RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
REDIS_HOST = os.environ['REDIS_HOST']

EXCEL_FILE_PATH = 'src/admin/Menu.xlsx'