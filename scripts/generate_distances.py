from vincenty import vincenty
import json
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

updb = mysql.connector.connect(
  host=str(os.environ.get('DB_HOST')),
  user=str(os.environ.get('DB_USERNAME')),
  password=str(os.environ.get('DB_PASSWORD')),
  database="prd_upark"
)

def rows_to_dict(cursor):
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

upc = updb.cursor(buffered=True)
get_buildings = ("SELECT id, latitude, longitude FROM building")
get_lots = ("SELECT id, latitude, longitude FROM lot")


upc.execute(get_buildings)
building_locations = rows_to_dict(upc)
# print(building_locations)
upc.execute(get_lots)
lot_locations = rows_to_dict(upc)
# print(lot_locations)

building_distances = {} # {building_id: {lot_id: distance}}

for building in building_locations:
  building_id = building['id']
  building_lat = building['latitude']
  building_long = building['longitude']
  cur_building_distances = {}
  # building_distances[building_id] = {}
  for lot in lot_locations:
    lot_id = lot['id']
    lot_lat = lot['latitude']
    lot_long = lot['longitude']
    if lot_lat < -90 or lot_lat > 90 or lot_long < -180 or lot_long > 180:
      print("Invalid lat/long: ", lot_lat, lot_long)
      print("Lot ID: ", lot_id)
      print("Building ID: ", building_id)
    if building_lat < -90 or building_lat > 90 or building_long < -180 or building_long > 180:
      print("Invalid lat/long: ", building_lat, building_long)
      print("Building ID: ", building_id)
      print("Lot ID: ", lot_id)
    distance_kilometers = vincenty((building_lat, building_long), (lot_lat, lot_long))
    distance_meters = distance_kilometers * 1000
    cur_building_distances[lot_id] = distance_meters
  building_distances[building_id] = cur_building_distances

print(json.dumps(building_distances, indent=2))

for building in building_distances:
  for lot in building_distances[building]:
    distance = building_distances[building][lot]
    upc.execute("INSERT INTO building_lot_distance (building_id, lot_id, distance) VALUES (%s, %s, %s)", (building, lot, distance))

if upc.warnings != None:
  print(upc.warnings)
  print(upc.warning_count)
else:
  updb.commit()
  print("Successfully inserted building distances")
