import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

DB = os.getenv('DB')
USER = os.getenv('USER')
PWD = os.getenv('PWD')

def connect():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        f'DATABASE={DB};'
        f'UID={USER};'
        f'PWD={PWD};'
        'Trusted_Connection=no;'
    )
    return conn
