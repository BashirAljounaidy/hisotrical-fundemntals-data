import pymysql
from sqlalchemy import create_engine, types
from finviz import get_stock
import pandas as pd
from mysql.connector import Error
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


host = os.getenv("HOST")
user = os.getenv("USERNAME")
passwd = os.getenv("PASSWORD")
db = os.getenv("DATABASE")
tablename = 'companies'

# data here
stock = get_stock('GOOG')

# opinion = dict(Date=str(pd.to_datetime('today'))[:10])
# stock.update(opinion)

# keys = '],['.join(stock.keys())
# question_marks = ','.join(list('?'*len(stock)))
# values = list(stock.values())
# cmd = "INSERT INTO "+tablename + " (["+keys+"]) VALUES ("+question_marks+")"
# cmd = str(cmd).replace('?', "%s")
# cmd = cmd.replace('[', "`").replace(']', "`")

# try:
#     connection = mysql.connector.connect(
#         host=host, database=db, user=user, password=passwd)
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         # cursor.execute(cmd, values)
#         connection.commit()
# except Error as e:
#     print("Error while connecting to MySQL", e)
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")


pymysql.install_as_MySQLdb()
engine = create_engine(
    f'mysql+mysqlconnector://{user}:{passwd}@{host}/{db}?charset=utf8mb4')

df = pd.DataFrame(stock.items())
df = df.T
df.columns = df.iloc[0]
df = df[1:]

df['Date'] = str(pd.to_datetime('today'))[:10]

# Convert the data types of the columns
df = df.convert_dtypes()
df = df.astype(str)
# Replace Excel_file_name with your excel sheet name
df.to_sql(tablename, con=engine, index=False, if_exists='append')
print("success")
