import requests
# import socket
# from contextlib import closing

# def check_socket(host, port):
#   with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
#     if sock.connect_ex((host, port)) == 0:
#       return True
#     else:
#       return False

# for i in range(0, 65535):
#   if check_socket("34.106.216.238", i):
#     print("Port", i, "is open")

# r = requests.get("https://upark-capstone.wm.r.appspot.com")
# r = requests.get("http://127.0.0.1:8080/lots")
# r = requests.get("http://34.106.216.238:8080")
r = requests.get("https://upark-web-server-a4uqmuxhda-wm.a.run.app/test")

print(r.text)