from flask import Flask, request, jsonify
import mysql.connector
import datetime
import math
from dotenv import load_dotenv
import os
import requests
load_dotenv()

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# print(os.environ.get('DB_HOST'))
# print(os.environ.get('DB_USERNAME'))
# print(os.environ.get('DB_NAME'))

updb = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=str(os.environ.get('DB_USERNAME')),
  password=str(os.environ.get('DB_PASSWORD')),
  database=str(os.environ.get('DB_NAME')) # TODO: Update gcloud env vars to include DB_NAME
)

upc = updb.cursor(buffered=True)

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

### Lots
lot_base_query = "SELECT id, name, latitude, longitude, car_count, stall_count, last_updated, enabled FROM lot"

@app.get("/lots")
def get_lots():
  lot_query = (lot_base_query)
  upc.execute(lot_query)
  lots = rows_to_dict(upc)
  print(lots)
  return jsonify(lots)

@app.get("/lots/<int:lot_id>")
def get_lot(lot_id):
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
  report_query = (report_base_query)
  upc.execute(report_query)
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

@app.get("/reports/<int:report_id>")
def get_report(report_id):
  report_query = (report_base_query + " WHERE id = %s")
  upc.execute(report_query, (report_id,))
  report = upc.fetchone()
  # print(report)
  return jsonify(report)

@app.get("/reports/lot/<int:lot_id>")
def get_reports_by_lot(lot_id):
  report_query = (report_base_query + " WHERE lot_id = %s")
  upc.execute(report_query, (lot_id,))
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

@app.get("/reports/user/<int:user_id>")
def get_reports_by_user(user_id):
  report_query = (report_base_query + " WHERE user_id = %s")
  upc.execute(report_query, (user_id,))
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

### Buildings
building_base_query = "SELECT id, name, latitude, longitude, street_address FROM building"

@app.get("/buildings")
def get_buildings():
  building_query = (building_base_query)
  upc.execute(building_query)
  buildings = rows_to_dict(upc)
  # print(buildings)
  return jsonify(buildings)

### Users

@app.get("/users/<int:user_id>")
def get_username(user_id):
  user_id_query = ("SELECT name, colorblind FROM user WHERE id = %s")
  upc.execute(user_id_query, (user_id,))
  username = upc.fetchone()
  # print(username)
  return jsonify(username)

# "POST" requests

@app.post("/report")
def post_report():
  print(request.json)
  user_id = request.json['user_id']
  time = request.json['time']
  lot_id = request.json['lot_id']
  longitude = request.json['longitude']
  latitude = request.json['latitude']
  approx_fullness = request.json['approx_fullness']
  report_query = ("INSERT INTO report (user_id, lot_id, longitude, latitude, time, approx_fullness) VALUES (%s, %s, %s, %s, %s, %s)")
  upc.execute(report_query, (user_id, lot_id, longitude, latitude, time, approx_fullness))
  updb.commit()
  update_lot_fullness(lot_id)
  return "Report added"

def update_lot_fullness(lot_id):
  # Get lot information
  lot_query = (lot_base_query + " WHERE id = %s")
  upc.execute(lot_query, (lot_id,))
  lot = upc.fetchone()
  if lot == None:
    return "Lot not found"
  lot_name = lot["name"]
  stall_count = lot["stall_count"]
  last_car_count = lot["car_count"]
  last_fullness = last_car_count / stall_count
  last_updated = lot["last_updated"]
  time_diff = datetime.datetime.now() - last_updated
  time_diff_hours = time_diff.total_hours()

  # Get last 3 reports
  reports_query = (report_base_query + " WHERE lot_id = %s ORDER BY time DESC limit 3")
  upc.execute(reports_query, (lot_id,))
  reports = upc.fetchall()
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
