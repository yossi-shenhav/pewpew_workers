#tasks.py
#from celery import Celery
import subprocess
import tempfile
import os
from celery.exceptions import SoftTimeLimitExceeded
# Assuming your Celery application is defined in a module named `celeryapp`
from celeryapp import celery
import json
from scanClass import Scan
from XSSScan import XSSScan
from Subdomain import SubdomainsScan
from FasrPortScan import FNmapScan, NmapScan
from LFIScan import LFIScan
from SSLScan import SSLScan
from NucleiScan import NucleiScan
from HiddenDirs import FfufScan
from firebase_reports import addNewScanData



# List all registered tasks
#print(app.tasks.keys())



# Define Celery task to process messages from the default queue
@celery.task(soft_time_limit=1600)
def exec_scan(scantype, tid, email, target ):
	try:
		return_code = 10
		results = {}
		scan = createScanObj(scantype, tid, email, target)
		
		commands = scan.getCommandsArr()
		for cmd in commands:
			result  = subprocess.run(cmd, shell=True, timeout=1600) 
			return_code = result.returncode
			print(f'command {cmd} finished with code:={return_code}')

		print(f'mission accomplished. id:={tid}')
		retval = {
			"scantype" : scantype,
			"id" : tid,
			"email" : email,
			"target" : target,
			"ret_code" : return_code
			}
		return retval
	except SoftTimeLimitExceeded:
		print ('timeout exceed') 
	


@celery.task()
def addScantoDB(message):
	msg = message
	scantype = msg['scantype']
	target =msg['target']
	email = msg['email']	
	tid = msg['id'] 
	success = True if msg['ret_code'] == 0 else False

	
	scan = createScanObj(scantype, tid, email, target)
	results = {}
	if success == True:
		results = scan.format_result()
	else:
		results["error"] = "Execution failed"
	scan.save_string_to_file(results, 'results5.json')	
	return_code = scan.addNewScanData(results)
	
	msg['ret_code'] = return_code
	return msg

@celery.task()
def sendEmail(message):
	msg = message
	scantype = msg['scantype']
	target =msg['target']
	email = msg['email']	
	tid = msg['id'] 
	success = True if msg['ret_code'] == 0 else False

	
	scan = createScanObj(scantype, tid, email, target)
	scan.uploadToS3() #do nothing at the moment - maybe add another task
	scan.sendMail(success)





def createScanObj(scantype, tid, email, target):
	#print (message)
	url = target
	match scantype:
		case 'XSS':
			scan = XSSScan(url, tid, email)
		case 'subdomain':
			scan = SubdomainsScan(url, tid, email)
		case 'PortScan':
			scan = NmapScan(url, tid, email)
		case 'FastPortScan':
			scan = FNmapScan(url, tid, email)
		case 'SSLScan':
			scan = SSLScan(url, tid, email)
		case 'LFI':
			scan =  LFIScan(url, tid, email)
		case 'hiddendir':
			scan = FfufScan(url, tid, email)
		case 'FullScan':
			#I think this should be nuclei
			scan = NucleiScan(url, tid, email)
		case _:
			#default is nmap - for now...
			print(f'\r\ndefault scan for type: {scantype}')
			scan = FNmapScan(url, tid, email)		
	   	
	    #upload_to_firebase(tid, f'~/consume/{tid}/asset_finder.txt') # uploading file to Firebase.
	    
	return scan


