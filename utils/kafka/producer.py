from pykafka.client import KafkaClient
import logging
import sys
import json
from pykafka.partitioners import hashing_partitioner
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable
from kafka import KafkaProducer


def kafka_saveLog(url, body):
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', )
    request = {"url": url, "state": body}
    msg = json.dumps(request)
    producer.send("topic", msg.encode(encoding='utf-8'))

