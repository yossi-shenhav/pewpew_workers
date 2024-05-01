import time
import random
import subprocess
import os
import uuid
import tldextract
import urllib.parse
from config1 import LIB_4_RESULTS, TIMEOUT_SEC
#from upload import upload_file_to_s3
from smtpmail import sendEmail
from firebase_reports import addNewScanData

class Scan:
	scan_type = None
	
	def __init__(self, target, scanid, email):
		if self.scan_type is None:
			raise NotImplementedError("Subclasses must implement scan_type")	

		self.return_code = -10 #not strated
		self.id = scanid
		self.target = target
		self.email = email
		self.directory = f'{LIB_4_RESULTS}{self.id}/{self.scan_type}'

	def execute_scan(self):
		try:
			os.makedirs(self.directory)
		except FileExistsError:
			#messages can be read more then once
			print('dir exist... not a problem')
		except Exception as e:
			print(f'error building {self.directory}', e)
		
		return self.run_commands()
		#raise NotImplementedError("Subclasses must implement execute_scan method.")
	


	
	def getCommands(self):
		raise NotImplementedError("Subclasses must implement getCommand method")
	
	
	def get_domain(self, subdomain):
		result = tldextract.extract(subdomain)
		domain = f'{result.domain}.{result.suffix}'
		return domain


	def run_commands(self):
		commands = self.getCommands()
		#print(commands)
		for cmd in commands:
			code = self.run_command(cmd)
		# I know it returns the code of last command
		# most of the times there is only one command
		# other time last command code is good enough
		# maybe we will change later
		return code


	
	def run_command(self, command):
		timeout_seconds = TIMEOUT_SEC
		poll_interval = 5  # Check status every 5 seconds

		start_time = time.time()

		process = subprocess.Popen(command, shell=True)
		#instead of witing for the process to complete, we check every few seconds
		while True:
			self.return_code = process.poll()

			if self.return_code is not None:
				# Process has completed
				print("Command completed with return code:", self.return_code)
				break

			current_time = time.time()
			elapsed_time = current_time - start_time

			if elapsed_time >= timeout_seconds:
			# Timeout reached
				print("Timeout reached. Terminating subprocess.")
				self.return_code = 5
				process.terminate()
				break

			# Sleep for the specified interval before checking again
			time.sleep(poll_interval)
		
		return self.return_code		
	
	def format_result(self):
		raise NotImplementedError("Subclasses must implement format_result method.")
	
	def urlEncode(self, str):
		return urllib.parse.quote(url)


	def sendEmail(self, success):
		return sendEmail(self.email, self.id, self.scan_type, success)
		
		
	def uploadToS3(self):
		s3obj = f'{self.id}/{self.scan_type}/{self.result_file}'
		file2upload = f'{self.directory}/{self.result_file}'
		success = True #upload_file_to_s3(file2upload, s3obj)
		return success
		print('not implemented yet')

	
	def addNewScanData(self, results):
		return addNewScanData(self.id, self.scan_type, self.target, results)




