import firebase_admin
import uuid
import hashlib
import os
from firebase_admin import credentials
from firebase_admin import db
import json


# Initialize Firebase Admin SDK

#shai - you should change to secret again
mounted_directory = '/cred/erviceAccountKey.json' #'/container/app/erviceAccountKey.json'

cred = credentials.Certificate(mounted_directory)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pewpew-7387e-default-rtdb.firebaseio.com/' 
})




def addNewScanData(scanid, scan_type, host, results):
	try:
		ref = db.reference(f'pewpew/reports/{scanid}')
		ref.child('hostname').set(host)
		print(f"nirza:\n\n{results}\n\n")
		ref.child(scan_type).set(results)
		return 0 #success 
	except Exception as e:
		print (f'\r\nresult:={results} --- host:={host} --- type:= {scan_type}\r\n')
		print (f'\r\nerror:={e}')
		return -1



def getScanData(scanid, scantype):
	ref = db.reference(f'pewpew/reports/{scanid}')
	scan_data = ref.get()

	if scan_data:
		
		rs = json.dumps(scan_data)
		hostname = scan_data.get('hostname', '')
		scantyperesults = scan_data.get(scantype, {})
		if not scantyperesults:
			return None
		else:
			results = scantyperesults["results"]
			return {'hostname': hostname, 'scantype': scantype, 'results': results}
	else:
		return None
        




# Example usage:
if __name__ == "__main__":
	results = { "results": {"openport1": 443, "openport2": 22, "openport3": 80}  }

	#addNewScanData("445", "nmap", "www.example.com", results) 	
	result = getScanData("445", "nmap")
	print (result)
	
	host = result["hostname"]
	st = result["scantype"]
	print(host + "****" + st)
	results = result["results"]	
	for port_key, port_value in results.items():
	    print(f"Port: {port_key}, Value: {port_value}")
	
