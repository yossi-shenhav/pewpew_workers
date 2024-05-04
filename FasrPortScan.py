
from scanClass import Scan
import xml.etree.ElementTree as ET


class FNmapScan(Scan):
	scan_type = 'FastPortScan'
	result_file = 'top100.xml'

	def format_result(self):
		result = {}
		if self.return_code == 0:
			open_ports = self.get_open_ports(self.directory + "/" + self.result_file)
			# Iterate through each port
			indx = 0
			for port in open_ports:
				indx +=1
				key = f'openport{indx}' 
				result[key] = port
		else:
			result['error'] = 'scan failed'
		
		return result

	def get_open_ports(self, xml_file):
		open_ports = []
		try:
			tree = ET.parse(xml_file)
			root = tree.getroot()
			for host in root.findall('host'):
				for port in host.findall(".//port"):
					state = port.find("state")
					if state is not None and state.attrib.get('state') == 'open':
						port_number = port.attrib['portid']
						open_ports.append(port_number)
		except Exception as e:
			print("Error parsing XML:", e)

		return open_ports

	def getCommands(self):
		commands = []
		commands = [f'nmap -F -oX {self.directory}/top100.xml {self.target}']	
		return commands


class NmapScan(Scan):
	scan_type = 'PortScan'
	result_file = 'top1000.xml'
	
	def format_result(self):
		result = {}
		if self.return_code == 0:
			open_ports = self.get_open_ports(self.directory + "/" + self.result_file)
			# Iterate through each port
			indx = 0
			for port in open_ports:
				indx +=1
				key = f'openport{indx}' 
				result[key] = port
			return result
		else:
			result['error'] = 'scan failed'		

	def get_open_ports(self, xml_file):
		open_ports = []
		try:
			tree = ET.parse(xml_file)
			root = tree.getroot()
			for host in root.findall('host'):
				for port in host.findall(".//port"):
					state = port.find("state")
					if state is not None and state.attrib.get('state') == 'open':
						port_number = port.attrib['portid']
						open_ports.append(port_number)
		except Exception as e:
			print("Error parsing XML:", e)

		return open_ports


	def getCommands(self):
		commands = []
		commands = [f'nmap -oX {self.directory}/top1000.xml {self.target}']	
		return commands
