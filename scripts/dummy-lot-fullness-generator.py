import mysql.connector
import datetime
from dotenv import load_dotenv
import os
import random
import math
load_dotenv()

updb = mysql.connector.connect(
  host="35.230.20.140",
  user=str(os.environ.get('dbUsername')),
  password=str(os.environ.get('dbPassword')),
  database="upark-data"
)
upc = updb.cursor(buffered=True)

# !!! IMPORTANT: This will override any reports that are already in the database !!!

### Dummy data generator ###
# This script will generate dummy heatmap data for the lots table

'''
Lot table structure
_________________________________________________________________________________________________________
| lot_id | lot_name | lot_lattitude | lot_longitude | fullness | car_count | stall_count | last_updated |
| uint   | varchar  | float         | float         | float    | uint      | uint        | datetime     |
---------------------------------------------------------------------------------------------------------
'''


# Get all lots (lot_id, lot_name)
upc.execute("SELECT lot_id, lot_name, stall_count FROM lots")
lots = []
for row in upc : lots.append(row)
print(lots)

# set report variables (eventually moved within loops)
update_time = datetime.datetime.now()

# TODO: Maybe add a random seed for reproducibility
# TODO: Add batching for faster generation

# Generate fullness values for each lot, and use that to fill fullness and car_count values
for lot in lots:
  lot_id = lot[0]
  lot_name = lot[1]
  stall_count = lot[2]
  fullness = min(1, max(0, random.gauss(0.75, 0.5)))
  car_count = math.floor(fullness * stall_count)
  print("Lot: {}, Fullness: {}, Car Count: {}, Stall Count: {}".format(lot_name, fullness, car_count, stall_count))

  # Update lot
  upc.execute("UPDATE lots SET fullness = %s, car_count = %s, last_updated = %s WHERE lot_id = %s", (fullness, car_count, update_time, lot_id))


# Check lot values
upc.execute("SELECT lot_id, lot_name, fullness, car_count, stall_count FROM lots WHERE last_updated = %s", (update_time, ))
for row in upc : print(row)

updb.commit()
