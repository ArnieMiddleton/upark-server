from flask import Flask, request, jsonify
import mysql.connector
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

def rows_to_dict(cursor):
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

updb = mysql.connector.connect(
  host="35.230.20.140",
  user=str(os.environ.get('dbUsername')),
  password=str(os.environ.get('dbPassword')),
  database="upark-data"
)
upc = updb.cursor(buffered=True)

app = Flask(__name__)

@app.get("/lots")
def get_lots():
  lot_query = ("SELECT lot_id, lot_name, lot_lattitude, lot_longitude, stall_count, car_count, fullness FROM lots")
  upc.execute(lot_query)
  lots = rows_to_dict(upc)
  # print(lots)
  return jsonify(lots)

@app.get("/reports")
def get_reports():
  report_query = ("SELECT report_id, time, lot_id, est_fullness, weight FROM reports")
  upc.execute(report_query)
  reports = rows_to_dict(upc)
  # print(reports)
  return jsonify(reports)