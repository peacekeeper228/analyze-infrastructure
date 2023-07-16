import psycopg2
from psycopg2 import pool
import os
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PoolConnections(object, metaclass=Singleton):
    def __init__(self):
        self.__postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 100,
            database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'], host='postgres', port=5432)
        
    def getConnection(self):
        return self.__postgreSQL_pool.getconn()

    def returnConnection(self, ps_connection):
        self.__postgreSQL_pool.putconn(ps_connection)