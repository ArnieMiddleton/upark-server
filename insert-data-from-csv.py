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

'''
Buildings
'''

# upc = updb.cursor(buffered=True)
# add_building = ("INSERT INTO buildings "
#                 "(bld_id, bld_name, bld_longitude, bld_lattitude, bld_strt_address, created_time)"
#                "VALUES (%s, %s, %s, %s, %s, %s)")

# data_buildings = []

# with open('buildings_data_final.csv', newline='\n') as csvfile:
#   reader = csv.reader(csvfile, delimiter=',')
#   for row in reader:
#     data_buildings.append(row)
#     print(row)

# for bld in data_buildings:
#   if bld[0] != "OBJECTID":
#     print(bld)
#     data_bld = (bld[0], bld[1], bld[5], bld[6], bld[4], datetime.datetime.now())
#     print(data_bld)
#     upc.execute(add_building, data_bld)

# query_bld = ("SELECT * FROM buildings")
# upc.execute(query_bld)

# for (bld_id, bld_name, bld_longitude, bld_lattitude, bld_strt_address, created_time) in upc:
#   print("{}, {}, {}, {}, {}, {}".format(bld_id, bld_name, bld_longitude, bld_lattitude, bld_strt_address, created_time))

# updb.commit()
