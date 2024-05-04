import json
from scanClass import Scan
from config1 import WORD_LIST, USER_AGENT, RECURSION_DEPTH


class FfufScan(Scan):
	scan_type = 'hidden-dirs'
	result_file = 'ffuf.json'
	log_file = 'ffuf.log'
	
	wordlist = WORD_LIST	
		
	def format_result(self):
		result = {}
		found = False
		if self.return_code == 0:					
			try:
				# Open the file and read the JSON data
				with open(f'{self.directory}/{self.result_file}', 'r') as file:
				    json_data = file.read()

				print(json_data)
				# Parse the JSON data
				data = json.loads(json_data)
				
				# Iterate over the results and print each one
				if 'results' in data and len(data['results']) > 0:
					for res in data['results']:
						#print(res)
						if 'url' in res and len(res['url'])>0:
							key = self.escapeFireBaseKey(res["url"])
							result[key] = res['status']
							found = True
						if found == False:		
							result['status'] = 'no results found'
				else:
					result['error'] = f'no results - check log file at {self.directory}'

			except Exception as e:
				print("An error occurred:", e) 
				result['error'] = e.args[0]
		else:
			result['error'] = 'scan failed'
		return result


	def getCommands(self):
		rnd_id = random.randint(1, 10000)
		log_file = f'{rnd_id}.txt'		
		commands = []
		commands = [f'ffuf -u https://{self.target}/FUZZ -w {self.wordlist} -H \'{USER_AGENT}\' -mc 200,204,301,302,307,401,405,500 -recursion -recursion-depth {RECURSION_DEPTH} -json -o {self.directory}/{self.result_file} -debug-log {self.directory}/{self.log_file}']
		return commands



	def escapeFireBaseKey(self, key):
		return self.urlEncode(key)
