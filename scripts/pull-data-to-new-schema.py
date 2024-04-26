import mysql.connector
import csv
import os

upark_data_updb = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=str(os.environ.get('DB_USERNAME')),
  password=str(os.environ.get('DB_PASSWORD')),
  database="upark-data"
)

upark_data_upc = upark_data_updb.cursor(buffered=True)
select_buildings = ("SELECT bld_id, bld_name, bld_longitude, bld_lattitude, bld_strt_address, created_time FROM buildings;")
upark_data_upc.execute(select_buildings)
data = upark_data_upc.fetchall()

# Create the csv file
with open('data/building.csv', 'w', newline='') as f_handle:
    writer = csv.writer(f_handle)
    # Add the header/column names
    header = ['id', 'name', 'longitude', 'latitude', 'street_address', 'enabled']
    writer.writerow(header)
    # Iterate over `data`  and  write to the csv file
    for row in data:
        row = list(row)
        row[len(row)-1] = 1
        writer.writerow(row)

select_lots = ("SELECT lot_id, lot_name, lot_longitude, lot_lattitude, car_count, stall_count, last_updated, fullness FROM lots;")
upark_data_upc.execute(select_lots)
data = upark_data_upc.fetchall()


# Create the csv file
with open('data/lot.csv', 'w', newline='') as f_handle:
    writer = csv.writer(f_handle)
    # Add the header/column names
    header = ['id', 'name', 'longitude', 'latitude', 'car_count', 'stall_count', 'last_updated', 'enabled']
    writer.writerow(header)
    # Iterate over `data`  and  write to the csv file
    for row in data:
        row = list(row)
        row[len(row)-1] = 1
        writer.writerow(row)