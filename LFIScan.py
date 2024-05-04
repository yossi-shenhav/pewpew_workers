from scanClass import Scan



class LFIScan(Scan):
	scan_type = 'LFI'
	result_file = 'lfi.json'
		
	def format_result(self):
		result = {}
		result['error'] = f'LFI not implmented'
				
		return result



	def getCommands(self):
		#I can implement in the subclass later - see if it works
		
		commands = []
		commands = [f'echo  "LFI Data" {self.directory}/{result_file}', 'sleep 8']	
		return commands
