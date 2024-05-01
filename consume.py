# consume.py
# This is the consumer script
import multiprocessing
import pika
import json #to parse the message - did not write the code here
import firebase_admin
import time
import subprocess
from scanClass import Scan
from XSSScan import XSSScan
from Subdomain import SubdomainsScan
from FasrPortScan import FNmapScan, NmapScan
from LFIScan import LFIScan
from SSLScan import SSLScan
from NucleiScan import NucleiScan
from HiddenDirs import FfufScan
from firebase_reports import addNewScanData
#from upload import upload_file_to_s3
from smtpmail import sendEmail
from config1 import read_secret, RABBIT_MQ, NUM_WORKERS




def worker():
	url = read_secret(RABBIT_MQ) 
	params = pika.URLParameters(url)

	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	channel.basic_qos(prefetch_count=1)
	channel.queue_declare(queue='nucleiscans')

	def callback(ch, method, properties, body):
		print(" [x] Received " + str(body))
		scan = parse_message(body)

		return_code = scan.execute_scan()

		#return_code is handled inrenaly
		results = scan.format_result()
		print (results)
		scan.addNewScanData(results)
		print ('added to db')
		#upload to S3
		success = scan.uploadToS3()
		#send mail
		scan.sendEmail(success)
		
		ch.basic_ack(delivery_tag=method.delivery_tag)
		print(f'mission accomplished. id:={scan.id}')

	def parse_message(message):
		#print (message)
		msg = json.loads(message)
		s_type = msg['email']
		url =msg['tid']
		email = msg['type']	# we should use it to send notification
		tid = msg['url2scan']    # transction id

		#scans = []
		#ALLOWED_TYPES = ['XSS', 'subdomain', 'PortScan', 'LFI', 'SSLScan', 'FullScan', 'hiddendir', 'FasrPortScan']
		match s_type:
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
				#for now I use nmap
				scan =  FNmapScan(url, tid, email)
			case 'hiddendir':
				scan = FfufScan(url, tid, email)
			case 'FullScan':
				#I think this should be nuclei
				scan = NucleiScan(url, tid, email)
			case _:
				#default is nmap - for now...
				print(f'\r\ndefault scan for type: {s_type}')
				scan = FNmapScan(url, tid, email)		
		   	
		    #upload_to_firebase(tid, f'~/consume/{tid}/asset_finder.txt') # uploading file to Firebase.
		    
		return scan


	channel.basic_consume(queue='nucleiscans', on_message_callback=callback, auto_ack=False)
	print("Worker started, waiting for messages...")
	channel.start_consuming()


def main():

	num_workers = NUM_WORKERS  # Set the number of workers
	processes = []
	for _ in range(num_workers):
		# Create a new process for each worker
		proc = multiprocessing.Process(target=worker)
		proc.start()
		print("Process PID:", proc.pid)
		processes.append(proc)

	# Wait for all workers to finish
	#for proc in processes:
	#	proc.join()






if __name__ == "__main__":
    main()

 

