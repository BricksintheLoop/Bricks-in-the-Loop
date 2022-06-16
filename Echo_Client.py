# Echo-client.py

import socket

HOST = "192.168.30.72"  #The server's hostname or IP address
PORT = 65432 # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    inp = input()
    s.sendall(str.encode(inp))
    data = s.recv(1024)

print(f"Received {data!r}")