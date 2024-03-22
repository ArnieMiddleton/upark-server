import requests

# r = requests.get("https://upark-capstone.wm.r.appspot.com")
# r = requests.get("http://127.0.0.1:8080/lots")
r = requests.get("http://34.106.216.238:8080")

print(r.text)