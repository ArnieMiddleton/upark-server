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

'''
Lots
'''

# upc = updb.cursor(buffered=True)
# data_lots = []

# with open('lots_data_final.csv', newline='\n') as csvfile:
#   reader = csv.reader(csvfile, delimiter=',')
#   for row in reader:
#     data_lots.append((row[0], row[1], row[5], row[6], row[2], datetime.datetime.now())) # lot_id, lot_name, lot_lattitude, lot_longitude, stall_count
#     print(row)
#     print(data_lots[-1])

# data_lots.remove(data_lots[0]) # remove the header

# add_lots = ("INSERT INTO lots "
#             "(lot_id, lot_name, lot_lattitude, lot_longitude, stall_count, car_count, fullness, last_updated)" "VALUES (%s, %s, %s, %s, %s, 0, 0.0, %s)")

# for lot in data_lots:
#   upc.execute(add_lots, lot)

# query_lots = ("SELECT * FROM lots")
# upc.execute(query_lots)

# for (lot_id, lot_name, lot_lattitude, lot_longitude, stall_count, last_updated, car_count, fullness) in upc:
#   print("{}, {}, {}, {}, {}, {}, {}, {}".format(lot_id, lot_name, lot_lattitude, lot_longitude, stall_count, last_updated, car_count, fullness))

# updb.commit()