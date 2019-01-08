from variables import *
import pymssql


sql="""create table epochtimes (ftitle text,furl text,fcontent text,fdate date)"""
target_cnx = pymssql.connect(host='localhost',user='postgres',password='wenqian628', database='postgres')
print('Database connected.')
target_cursor = target_cnx.cursor()
target_cursor.execute(sql)
target_cnx.commit()
target_cursor.close()
target_cnx.close()

