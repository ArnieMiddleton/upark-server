import csv
import mysql.connector
import os

upark_data_updb = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=str(os.environ.get('DB_USERNAME')),
  password=str(os.environ.get('DB_PASSWORD')),
  database="prd_upark"
)

upark_data_upc = upark_data_updb.cursor(buffered=True)

with open ('data/building.csv', 'r') as f:
  reader = csv.reader(f)
  columns = next(reader)
  columns_str = ', '.join(columns)
  values_str = ('%s, ' * len(columns))[0:-2]
  query = 'INSERT INTO building ({0}) VALUES ({1})'.format(columns_str, values_str)
  error = False
  for data in reader:
    try:
      upark_data_upc.execute(query, data)
    except mysql.connector.Error as err:
      error = True
      print(err)
  if not error:
    upark_data_updb.commit()

with open('data/lot.csv', 'r') as f:
  reader = csv.reader(f)
  columns = next(reader)
  columns_str = ', '.join(columns)
  values_str = ('%s, ' * len(columns))[0:-2]
  query = 'INSERT INTO lot ({0}) VALUES ({1})'.format(columns_str, values_str)
  error = False
  for data in reader:
    try:
      upark_data_upc.execute(query, data)
    except mysql.connector.Error as err:
      error = True
      print(err)
  if not error:
    upark_data_updb.commit()