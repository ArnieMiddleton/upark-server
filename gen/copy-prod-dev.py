import mysql.connector
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

updb = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=str(os.environ.get('DB_USERNAME')),
  password=str(os.environ.get('DB_PASSWORD'))
)

upc = updb.cursor(buffered=True)

upc.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='prd_upark';")
tables = upc.fetchall()

error = False
for table in tables:
  print("Copying " + table[0] + " from prd to dev")
  try:
    upc.execute("CREATE TABLE IF NOT EXISTS dev_upark." + table[0] + " LIKE prd_upark." + table[0] + ";")
    if upc.warnings:
      print(upc.warnings)
    upc.execute("INSERT IGNORE INTO dev_upark." + table[0] + " SELECT * FROM prd_upark." + table[0] + ";")
    if upc.warnings:
      print(upc.warnings)
  except mysql.connector.Error as err:
    error = True
    print("Error copying table " + table[0] + " from prd to dev with error: " + str(err))

if not error:
  updb.commit()