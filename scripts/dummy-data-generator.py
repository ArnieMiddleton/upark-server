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

### Dummy data generator ###
# This script will generate dummy data for the reports table
# It will generate reports for each lot in the lots table

## Constants ##
rpl = 12 # reports per lot
dummy_id = 0 # dummy user
## End Constants ##

'''
Report table structure
___________________________________________________________________
| user_id | eport_id | time     | lot_id  | est_fullness | weight |
| uint fk | uint     | datetime | uint fk | float        | uint   |
-------------------------------------------------------------------
|         |          |          |         |              |        |
|         |          |          |         |              |        |
|         |          |          |         |              |        |
-------------------------------------------------------------------
'''

'''
# TEMPORARY #
# Create dummy user for dummy reports
add_user = ("INSERT INTO users "
            "(user_id, username, user_fname, user_lname, created_time, last_edited_time)"
            "VALUES (%s, %s, %s, %s, %s, %s)")
data_user = (dummy_id, "dummy", "dummy", "dummy", datetime.datetime.now(), datetime.datetime.now())
upc.execute(add_user, data_user)

upc.execute("SELECT * FROM users WHERE user_id = {}".format(dummy_id))
for row in upc : print(row)

updb.commit()
# END TEMP #
'''


# Get all lots (lot_id, lot_name)
upc.execute("SELECT lot_id, lot_name FROM lots")
lots = []
for row in upc : lots.append(row)
print(lots)

# First, clear all reports by dummy user
upc.execute("DELETE FROM reports WHERE user_id = {}".format(dummy_id))

# Generate dummy reports
# add_report = ("INSERT INTO reports "
#               "(user_id, time, lot_id, est_fullness, weight)"
#               "VALUES (%s, %s, %s, %s, %s)")

# set report variables (eventually moved within loops)
report_time = datetime.datetime.now()
weight = 1
user_id = dummy_id

# Basic batching implemented
#TODO: Improve batching performance

# For each lot, generate rpl reports
for lot in lots:
  add_report_values = ("(%s, %s, %s, %s, %s), " * rpl)[:-2] # remove trailing comma and space
  add_report = ("INSERT INTO reports "
                "(user_id, time, lot_id, est_fullness, weight)"
                "VALUES {}".format(add_report_values))
  full_lot_report_data = []
  for i in range(rpl):
    # Generate report data
    # Use current time for now, eventually generate rpl different times so each report is unique and can be used to track changes over time
    # Generate random fullness
    # Use weight of 1 and dummy user (user_id) for now
    # Don't need to generate report_id, it's auto-incremented
    lot_id = lot[0]
    est_fullness = min(1, max(0, random.gauss(0.75, 0.5))) # random distributed around 0.75, clamped to [0, 1]
    report_data = (user_id, report_time, lot_id, est_fullness, weight)
    # print(report_data)
    # upc.execute(add_report, report_data)
    for data in report_data: full_lot_report_data.append(data)
  upc.execute(add_report, full_lot_report_data)


# Check reports
upc.execute("SELECT * FROM reports WHERE user_id = {}".format(dummy_id))
for row in upc : print(row)

updb.commit()
