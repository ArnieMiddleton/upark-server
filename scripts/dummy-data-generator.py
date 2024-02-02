import mysql.connector
import datetime
import csv
from dotenv import load_dotenv
import os
load_dotenv()

updb = mysql.connector.connect(
  host="35.230.20.140",
  user=str(os.environ.get('dbUsername')),
  password=str(os.environ.get('dbPassword')),
  database="upark-data"
)
upc = updb.cursor(buffered=True)

'''
Report Dummy Data
'''

