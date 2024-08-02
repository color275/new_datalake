from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *

import os

DBUSER = os.getenv("DBUSER")
PASSWORD = os.getenv("PASSWORD")
PRIMARY_HOST = os.getenv("PRIMARY_HOST")
PRIMARY_PORT = os.getenv("PRIMARY_PORT")
PRIMARY_DBNAME = os.getenv("PRIMARY_DBNAME")

READONLY_HOST = os.getenv("READONLY_HOST")
READONLY_PORT = os.getenv("READONLY_PORT")
READONLY_DBNAME = os.getenv("READONLY_DBNAME")

# PostgreSQL URL
PRIMARY_DB_URL = f'postgresql+psycopg2://{DBUSER}:{PASSWORD}@{PRIMARY_HOST}:{PRIMARY_PORT}/{PRIMARY_DBNAME}?options=-c%20search_path=ecommerce'
READONLY_DB_URL = f'postgresql+psycopg2://{DBUSER}:{PASSWORD}@{READONLY_HOST}:{READONLY_PORT}/{READONLY_DBNAME}?options=-c%20search_path=ecommerce'


class PrimaryEngineConn:
    def __init__(self):
        self.engine = create_engine(
            PRIMARY_DB_URL, pool_size=100, max_overflow=10, pool_recycle=100)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()


class ReadonlyEngineConn:
    def __init__(self):
        self.engine = create_engine(
            READONLY_DB_URL, pool_size=100, max_overflow=10, pool_recycle=100)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()
