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
from ShodanScan import ShodanScan
from Subdomain import SubdomainsScan
from FasrPortScan import FNmapScan, NmapScan
from LFIScan import LFIScan
from SSLScan import SSLScan
from NucleiScan import NucleiScan
from HiddenDirs import FfufScan
from firebase_reports import addNewScanData
# from config1 import SCAN_TIME_LIMIT
from celery import group

SCAN_TIME_LIMIT = 1600


# List all registered tasks
#print(app.tasks.keys())



# Define Celery task to process messages from the default queue
@celery.task(soft_time_limit=SCAN_TIME_LIMIT)
def exec_scan(scantype, tid, email, target , id=None):
	try:
		return_code = 10
		results = {}
		print(f'\n\nThis is: {scantype}\n\n')
		scan = createScanObj(scantype, tid, email, target, id)
		print('exec_scan started')
		
		commands = scan.getCommandsArr()
		for cmd in commands:
			print(f'cmd:={cmd}')
			timeout = SCAN_TIME_LIMIT + 10 #probably we don't need timeout at all
			result  = subprocess.run(cmd, shell=True, timeout=timeout) 
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
	
def process_in_batches(scantype, tid, email, targets, batch_size=50):
    batches = [targets[i:i + batch_size] for i in range(0, len(targets), batch_size)]
    id = 0
    for batch_num, batch in enumerate(batches):
        id = id + 1
        print(f"Processing batch {batch_num + 1}/{len(batches)} with {len(batch)} targets...")
        batch_tasks = group(exec_scan.s(scantype, tid, email, target, id+tempId) for tempId, target in enumerate(batch))
        result = batch_tasks.apply_async()
        result.join()  # Wait for the batch to complete before moving to the next batch
        print(f"Batch {batch_num + 1}/{len(batches)} completed.")



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
	#scan.save_string_to_file(results, 'results5.json')
	print(f"nirza1:\n\n{results}\n\n")	
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





def createScanObj(scantype, tid, email, target, id):
	#print (message)
	print('AAAAAAAAAA')
	url = target
	print(f"\n\nThe scantype is: {scantype}\n\n")
	match scantype:
		case 'shodan':
			scan = ShodanScan(url, tid, email, id)
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
			print('BBBBBBBBBBB')
			print(f'\r\ndefault scan for type: {scantype}')
			scan = FNmapScan(url, tid, email)		
	   	
	    #upload_to_firebase(tid, f'~/consume/{tid}/asset_finder.txt') # uploading file to Firebase.
	    
	return scan


