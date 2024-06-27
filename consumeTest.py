# consume.py
# This is the consumer script
import pika
import json #to parse the message - did not write the code here
from config1 import read_secret, RABBIT_MQ, NUM_WORKERS, RABBIT_MQ_LOCAL
from celeryapp import celery
from tasks import exec_scan, addScantoDB, sendEmail, process_in_batches


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


def test_start_message(body):
	print(" [x] Received " + str(body))
	
	msg = json.loads(body)
	s_type = msg['type']
	target =msg['url2scan']
	email = msg['email']	# we should use it to send notification
	tid = msg['tid']    # transction id


	result = process_in_batches(s_type, tid, email, target)

	# result = exec_scan.delay(s_type, tid, email, target)
	# result = exec_scan.apply_async(args=[s_type, tid, email, target])

	# Chain task2 and task3 to start after task1 completes
	# result2 = addScantoDB.apply_async(args=[result.get()]) # Passes result of task1 to task2
	# sendEmail.apply_async(args=[result2.get()])
	






if __name__ == "__main__":

	import json

	# Define your dictionary
	body_XSS = {
		'type': 'XSS',
		'url2scan': 'xss.challenge.training.hacq.me/challenges/baby01.php',
		'email': 'nirza@nirza.com',
		'tid': 2
	}

	body = {
		'type': 'shodan',
		'url2scan': ["20.204.225.50","4.224.127.227","20.204.224.250"],
		'email': 'nirza@nirza.com',
		'tid': 2
	}

	# Convert dictionary to JSON string
	msg_body = json.dumps(body)



	test_start_message(msg_body)

	# url = read_secret(RABBIT_MQ) 
	# params = pika.URLParameters(url)

	# connection = pika.BlockingConnection(params)
	# channel = connection.channel()
	# channel.basic_qos(prefetch_count=1)
	# channel.queue_declare(queue='nucleiscans')

	# channel.basic_consume(queue='nucleiscans', on_message_callback=callback)
	# print("Worker started, waiting for messages...")
	# channel.start_consuming()

 

