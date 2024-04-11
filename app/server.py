from flask import Flask, request, jsonify
import mysql.connector
import datetime
from dotenv import load_dotenv
import os
import requests
load_dotenv()

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

print(os.environ.get('DB_HOST'))

updb = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=str(os.environ.get('DB_USERNAME')),
  password=str(os.environ.get('DB_PASSWORD')),
  database="upark-data"
)
print(updb)
print(updb.is_connected())
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

@app.get("/test")
def test():
  return jsonify("Test successful")

@app.get("/")
def home():
  return jsonify("Welcome to the UPark API")

@app.get("/lots")
def get_lots():
  lot_query = ("SELECT lot_id, lot_name, lot_lattitude, lot_longitude, stall_count FROM lots")
  upc.execute(lot_query)
  lots = rows_to_dict(upc)
  # print(lots)
  return jsonify(lots)

@app.get("/lots/<int:lot_id>")
def get_lot(lot_id):
  lot_query = ("SELECT lot_id, lot_name, lot_lattitude, lot_longitude, stall_count FROM lots WHERE lot_id = %s")
  upc.execute(lot_query, (lot_id,))
  lot = upc.fetchone()
  # print(lot)
  return jsonify(lot)

@app.get("/lots/<string:lot_name>")
def get_lot_id(lot_name):
  lot_query = ("SELECT lot_id FROM lots WHERE lot_name = %s")
  upc.execute(lot_query, (lot_name,))
  lot_id = upc.fetchone()
  # print(lot_id)
  return jsonify(lot_id)

@app.get("/reports")
def get_reports():
  report_query = ("SELECT report_id, time, lot_id, est_fullness, weight FROM reports")
  upc.execute(report_query)
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)

@app.get("/buildings")
def get_buildings():
  building_query = ("SELECT bld_id, bld_name, bld_longitude, bld_lattitude, bld_strt_address FROM buildings")
  upc.execute(building_query)
  buildings = rows_to_dict(upc)
  # print(buildings)
  return jsonify(buildings)

@app.get("/user/<int:user_id>")
def get_username(user_id):
  user_id_query = ("SELECT username FROM users WHERE user_id = %s")
  upc.execute(user_id_query, (user_id,))
  username = upc.fetchone()
  # print(username)
  return jsonify(username)

# "POST" requests

@app.post("/report")
def post_report():
  user_id = request.json['user_id']
  time = request.json['time']
  lot_id = request.json['lot_id']
  est_fullness = request.json['est_fullness']
  report_query = ("INSERT INTO reports (user_id, time, lot_id, est_fullness, weight) VALUES (%s, %s, %s, %s, %s)")
  upc.execute(report_query, (user_id, time, lot_id, est_fullness, 1))
  updb.commit()
  update_lot_fullness(lot_id)
  return "Report added"

def update_lot_fullness(lot_id):
  lot_query = ("SELECT lot_name, stall_count, car_count, fullness, last_updated FROM lots WHERE lot_id = %s")
  upc.execute(lot_query, (lot_id,))
  lot = upc.fetchone()
  if lot == None:
    return "Lot not found"
  lot_name = lot[0]
  stall_count = lot[1]
  last_car_count = lot[2]
  last_fullness = lot[3]
  last_updated = lot[4]
  time_diff = datetime.datetime.now() - last_updated
  time_diff_hours = time_diff.total_hours()
  # TODO: Add more complex moving average algorithm
  reports_query = ("SELECT est_fullness FROM reports ORDER BY time DESC limit 3 WHERE lot_id = %s")
  upc.execute(reports_query)
  reports = upc.fetchall()
  if len(reports) == 0:
    return "No reports found"
  est_fullness = sum(reports) / len(reports) # simple average of last 3 reports
  car_count = est_fullness * stall_count
  # Update lot
  update_query = ("UPDATE lots SET car_count = %s, fullness = %s, last_updated = %s WHERE lot_id = %s")
  upc.execute(update_query, (car_count, est_fullness, datetime.datetime.now(), lot_id))
  updb.commit()
  return "Lot updated"
