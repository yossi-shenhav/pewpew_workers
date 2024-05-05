#import time
#import random
import subprocess
import os
#import uuid
import tldextract
import urllib.parse
from config1 import LIB_4_RESULTS, TIMEOUT_SEC
#from upload import upload_file_to_s3
from smtpmail import sendEmail
from firebase_reports import addNewScanData

class Scan:
	scan_type = None
	result_file = None
	
	def __init__(self, target, scanid, email):
		if self.scan_type is None:
			raise NotImplementedError("Subclasses must implement scan_type")	
		if self.result_file is None:
			raise NotImplementedError("Subclasses must implement result_file")	
			
		self.return_code = 0 #not used anymore, but did not want to change all derived classes
		self.id = scanid
		self.target = target
		self.email = email
		self.directory = f'{LIB_4_RESULTS}{self.id}/{self.scan_type}'

	
	def getCommands(self):
		raise NotImplementedError("Subclasses must implement getCommand method")
	
	
	def get_domain(self, subdomain):
		result = tldextract.extract(subdomain)
		domain = f'{result.domain}.{result.suffix}'
		return domain


	def getCommandsArr(self):
		commands = self.getCommands()
		commands.insert(0, f'rm {self.directory}/{self.result_file}')
		commands.insert(0, f'mkdir -p {self.directory}')
		return commands

			
	
	def format_result(self):
		raise NotImplementedError("Subclasses must implement format_result method.")
	
	def urlEncode(self, str, safe=False):
		#maybe we should always use safe=True
		#since the default is false I left the default
		if safe:
			return urllib.parse.quote(url, safe="")
		else:
			return urllib.parse.quote(url)
		


	def sendMail(self, success):
		return sendEmail(self.email, self.id, self.scan_type, success)
		
		
	def uploadToS3(self):
		s3obj = f'{self.id}/{self.scan_type}/{self.result_file}'
		file2upload = f'{self.directory}/{self.result_file}'
		success = True #upload_file_to_s3(file2upload, s3obj)
		return success
		print('not implemented yet')

	
	def addNewScanData(self, results):
		return addNewScanData(self.id, self.scan_type, self.target, results)




