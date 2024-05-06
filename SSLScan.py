from scanClass import Scan
import json

#
class SSLScan(Scan):
	scan_type = 'SSLScan'
	result_file = 'ssl_result.json'

		
	def format_result(self):
		result = {}
		if self.return_code == 0:
			try:
				# Open the file and read the JSON data
				with open(self.directory + "/" + self.result_file, 'r') as file:
					json_data = file.read()
				# Parse JSON data
				data = json.loads(json_data)

				# Filter elements where severity is not INFO or OK
				filtered_elements = [elem for elem in data if elem['severity'] not in ['INFO', 'OK'] or elem['id'] in ['grade_cap_reason_1', 'final_score', 'overall_grade', 'cipher_strength_score']]
				# Print filtered elements
				for elem in filtered_elements:
					print(f"id:={elem['id']} encoded:={self.encodeFirebase_key(elem['id'])}")
					print(f"value:={elem['finding']} encoded:={self.encodeFirebase_key(elem['finding'])}")
					
					result[self.encodeFirebase_key(elem['id'])] = self.encodeFirebase_key(elem['finding'])
					#result[elem['id']] = elem['finding']
			except Exception as e:
				print("An error occurred:", e) 
				result['error'] = e.args[0]
		else:
			result['error'] = ' scan failed'		
		return result
	
	def getCommands(self):		
		commands = []
		commands = [f'/home/parallels/Documents/testssl.sh/testssl.sh --jsonfile {self.directory}/{self.result_file} {self.target}']
		#commands = [f'testssl --jsonfile {self.directory}/{self.result_file} {self.target}']

		return commands
