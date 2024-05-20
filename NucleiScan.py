from scanClass import Scan
from config1 import NUCLEI_PREFIX 

class NucleiScan(Scan):
	scan_type = 'FullScan'
	result_file = 'vuln.txt'

	def format_result(self):
		result = {}
		if self.return_code == 0:
			try:
				# Open the file and read the JSON data
				with open(self.directory + "/" + self.result_file, 'r') as file:
					lines = [line.strip() for line in file]				
				indx = 0
				for ln in lines:
					words = ln.split()
					key = self.encodeFirebase_key(words[0])
					value = self.encodeFirebase_key(' '.join(words[1:]))
					result[key] = value
			except Exception as e:
				print("An error occurred:", e) 
				result['error'] = self.encodeFirebase_key(e.args[0])
		else:
			result['error'] = 'scan failed'		
		return result


	def getCommands(self):		
		commands = []
		prefix = NUCLEI_PREFIX
		commands = [f'nuclei -u {prefix}{self.target} -o {self.directory}/{self.result_file} -es info']
		return commands


