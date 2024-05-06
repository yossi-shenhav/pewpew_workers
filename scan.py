from scanClass import Scan
from XSSScan import XSSScan
from Subdomain import SubdomainsScan
from FasrPortScan import FNmapScan
from LFIScan import LFIScan
from SSLScan import SSLScan
from HiddenDirs import FfufScan
from firebase_reports import addNewScanData

import uuid
import time
import random

if __name__ == "__main__":
	scan = SSLScan('test.com', 68, 'yossi@komodosec.com')
	results = scan.format_result()
	return_code = scan.addNewScanData(results)			
	#for scan in scans:
	#	results = scan.format_result()
	#	print (results)
	#	addNewScanData(scan.id, scan.scan_type, scan.target, results)
		 		
	print(f'mission accomplished. cnt:={return_code}')

