import os
import threading

from kafka import KafkaConsumer
from utils.save import *
import time
from utils.nats.subscriber import *

def kafka_consumer():
    th = threading.Thread(target=NATS_subscribe)
    th.start()
    consumer = KafkaConsumer('topic', bootstrap_servers=['127.0.0.1:9092'])
    filename = "D:\\study\\python\\cmdb-python\\log\\logTest.txt"
    lines = ""

    for msg in consumer:
        recv = time.asctime(time.localtime(time.time())) + "  %s:%d:%d: key=%s value=%s" % (
            msg.topic, msg.partition, msg.offset, msg.key, str(msg.value, encoding='utf-8'))
        lines += recv + "\n"
        print(recv)
        saveInfoAsFile(lines, filename)


if __name__ == '__main__':
    kafka_consumer()
