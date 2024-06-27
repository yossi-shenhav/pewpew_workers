from scanClass import Scan
import random
import os
from utils.shodanScan import query_shodan_for_host

class ShodanScan(Scan):
	scan_type = 'shodan'
	result_file = 'shodan_results.txt'
	error_file = 'shodan_erros.txt'
	
	
	def format_result(self):
		result = {}
		print("shodan scan starts")
		if self.return_code == 0:
			try:
				# Open the file and read the JSON data
				with open(self.directory + "/" + self.result_file, 'r') as file:
					lines = [line.strip() for line in file]
				print (f'lines:={lines}')			
				indx = 0
				for i, ln in enumerate(lines):
					print(f'ln:={ln}')
					arr = ln.split()
					key = arr[0][1:-1]
					keyarr = key.split("][")
					key = str(i) + "_" + keyarr[-1]
					print(f'key:={key}')
					result[key] = arr[1]
			except Exception as e:
				print("An error occurred:", e) 
				result['error'] = e.args[0]
		else:
			result['error'] = f'scan failed with code {self.return_code}'

		print(f"nirza2:\n\n{result}\n\n")	
		return result

		
	def getCommands(self):
		#I can implement in the subclass later - see if it works
		# rnd_id = random.randint(1, 10000)
		commands = []
		commands = [f'shodan host {self.target} | tee {self.directory}/shodan_results.txt']	
		return commands



