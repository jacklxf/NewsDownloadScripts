from sqlalchemy import create_engine
import pymssql

host='localhost'
dbname='postgres'
user='postgres'
password='wenqian628'
engine = create_engine('postgresql://postgres:wenqian628@localhost:5432/postgres')
