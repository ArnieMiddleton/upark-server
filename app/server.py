from flask import Flask, request, jsonify
import mysql.connector
import datetime
import math
from dotenv import load_dotenv
import os
import requests
load_dotenv()

app = Flask(__name__)

host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
database = os.environ.get('DB_NAME')

databaseName = os.environ.get('DB_NAME').split("_")[0]


if __name__ == "__main__":
  # app.run(debug=True)
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)),ssl_context=('cert.pem', 'key.pem'))


def rows_to_dict(cursor):
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

# "GET" requests

@app.get("/")
def home():
  return jsonify("Welcome to the UPark API")

@app.get("/info")
def info():
  ret = jsonify(name="Upark API", database=databaseName)
  print(ret)
  return ret

### Lots
lot_base_query = "SELECT id, name, latitude, longitude, car_count, stall_count, last_updated, enabled FROM lot"

@app.get("/lots")
def get_lots():
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  lot_query = (lot_base_query)
  upc.execute(lot_query)
  lots = rows_to_dict(upc)
  # print(lots)
  return jsonify(lots)

@app.get("/lots/<int:lot_id>")
def get_lot(lot_id):
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  lot_query = (lot_base_query + " WHERE id = %s")
  upc.execute(lot_query, (lot_id,))
  lot = upc.fetchone()
  # print(lot)
  return jsonify(lot)

'''
@app.get("/lots/<string:lot_name>")
def get_lot_id(lot_name):
  lot_query = (lot_base_query + " WHERE lot_name = %s")
  upc.execute(lot_query, (lot_name,))
  lot_id = upc.fetchone()
  # print(lot_id)
  return jsonify(lot_id)
'''

### Reports
report_base_query = "SELECT id, lot_id, latitude, longitude, time, approx_fullness, weight FROM report"

@app.get("/reports")
def get_reports():
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  report_query = (report_base_query)
  upc.execute(report_query)
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

@app.get("/reports/<int:report_id>")
def get_report(report_id):
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  report_query = (report_base_query + " WHERE id = %s")
  upc.execute(report_query, (report_id,))
  report = upc.fetchone()
  # print(report)
  return jsonify(report)

@app.get("/reports/lot/<int:lot_id>")
def get_reports_by_lot(lot_id):
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  report_query = (report_base_query + " WHERE lot_id = %s")
  upc.execute(report_query, (lot_id,))
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

@app.get("/reports/user/<string:user_id>")
def get_reports_by_user(user_id):
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  report_query = (report_base_query + " WHERE user_id = %s")
  upc.execute(report_query, (user_id,))
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

### Buildings
building_base_query = "SELECT id, name, code, latitude, longitude, street_address FROM building"

@app.get("/buildings")
def get_buildings():
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  building_query = (building_base_query)
  upc.execute(building_query)
  buildings = rows_to_dict(upc)
  # print(buildings)
  return jsonify(buildings)

### Users

@app.get("/users/<string:user_id>")
def get_user(user_id):
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  user_query = ("SELECT id, name, colorblind FROM user WHERE id = %s LIMIT 1")
  upc.execute(user_query, (user_id,))
  fetched_user = rows_to_dict(upc).pop()
  print(fetched_user)
  return jsonify(fetched_user)

# "POST" requests

@app.post("/report")
def post_report():
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  print(request.json)
  try:
    user_id = request.json['user_id']
    time = request.json['time']
    lot_id = request.json['lot_id']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    approx_fullness = request.json['approx_fullness']
  except Exception as e:
    print("Error in converting request to json: " + str(e))
    return "Error in converting request to json"
  try:
    report_query = ("INSERT INTO report (user_id, lot_id, longitude, latitude, time, approx_fullness) VALUES (%s, %s, %s, %s, %s, %s)")
    upc.execute(report_query, (user_id, lot_id, longitude, latitude, time, approx_fullness))
    print("Report added: " + str(upc.lastrowid))
    print("Report result: " + str(upc.warnings))
    updb.commit()
  except Exception as e:
    print("Error in adding report: " + str(e))
    return "Error in adding report"
  update_lot_fullness(lot_id)
  return "Report added"


#id, name, latitude, longitude, car_count, stall_count, last_updated, enabled
def update_lot_fullness(lot_id):
  updb = mysql.connector.connect(host=host, user=user, password=password, database=database)
  upc = updb.cursor(buffered=True)
  # Get lot information
  lot_query = (lot_base_query + " WHERE id = %s")
  upc.execute(lot_query, (lot_id,))
  lot = rows_to_dict(upc).pop()
  if lot == None:
    return "Lot not found"
  lot_name = lot["name"]
  stall_count = lot["stall_count"]
  last_car_count = lot["car_count"]
  last_fullness = last_car_count / stall_count
  last_updated = lot["last_updated"]
  time_diff = datetime.datetime.now() - last_updated
  # time_diff_hours = time_diff.total_hours()

  # Get last 3 reports
  reports_query = (report_base_query + " WHERE lot_id = %s ORDER BY time DESC limit 3")
  upc.execute(reports_query, (lot_id,))
  reports = rows_to_dict(upc)
  if len(reports) == 0:
    return "No reports found"
  # TODO: Add more complex moving average algorithm
  approx_fullness = sum([report["approx_fullness"] for report in reports]) / len(reports) # simple average of last 3 reports
  car_count = math.floor(approx_fullness * stall_count)

  # Update lot
  update_query = ("UPDATE lot SET car_count = %s, last_updated = %s WHERE id = %s")
  upc.execute(update_query, (car_count, datetime.datetime.now(), lot_id))
  updb.commit()
  return "Lot {lot_name} ({lot_id}) updated to {car_count} cars ({approx_fullness} fullness) from {last_car_count} cars ({last_fullness} fullness) over {time_diff_hours} hours"
