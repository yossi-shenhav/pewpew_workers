# consume.py
# This is the consumer script
import pika
import json #to parse the message - did not write the code here
from config1 import read_secret, RABBIT_MQ, NUM_WORKERS, RABBIT_MQ_LOCAL
from celeryapp import celery
from tasks import exec_scan, addScantoDB, sendEmail


def callback(ch, method, properties, body):
	print(" [x] Received " + str(body))
	
	msg = json.loads(body)
	s_type = msg['type']
	target =msg['url2scan']
	email = msg['email']	# we should use it to send notification
	tid = msg['tid']    # transction id

	#result = exec_scan.delay(s_type, tid, email, target)
	result = exec_scan.apply_async(args=[s_type, tid, email, target])

	# Chain task2 and task3 to start after task1 completes
	result2 = addScantoDB.apply_async(args=[result.get()]) # Passes result of task1 to task2
	sendEmail.apply_async(args=[result2.get()])
	
	print(f'mission accomplished uuid={tid}')
	ch.basic_ack(delivery_tag=method.delivery_tag)






if __name__ == "__main__":
	
	result = exec_scan.apply_async(args=["XSS", 1234, "nir.zadok@komodosec.com", "something.me"])
