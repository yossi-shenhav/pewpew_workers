# celeryapp.py
from celery import Celery
from celeryconfig import *
#from celery.exceptions import SoftTimeLimitExceeded
from config1 import RABBIT_MQ_LOCAL, read_secret


broker_url = read_secret(RABBIT_MQ_LOCAL)
#print(broker_url)
celery = Celery('tasks', broker=broker_url,     include=CELERY_IMPORTS )


celery.conf.update(
    result_backend='rpc',  # Use RPC result backend
    task_serializer='json',  # Use JSON serialization for tasks
    accept_content=['json'],  # Accept only JSON content
    task_default_queue = 'celerytasks',  # Set the default queue for Celery to consume messages from
)
