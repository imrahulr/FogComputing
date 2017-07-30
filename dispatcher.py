# dispatcher.py

import threading
import sys
import pipes
import paho.mqtt.client as mqtt
import json


global buff
buff = []


def pipe_readder(topic):
    global buff
    while True:
        pipe = pipes.pipes('sub', topic)
        msg = pipe.read_pipes()
        buff.append(msg)


def pubb(topic_serv):
    global buff
    while True:
        if len(buff) != 0:
            msg = buff.pop(0)
            mqttc.publish(topic_serv, msg)


if __name__ == '__main__':
    print("dispatcher.py started")
    mqttc = mqtt.Client()
    app = sys.argv[1]
    f = open(str(app)+'.txt', 'r')
    app_config = f.read()
    f.close()
    app_config = json.loads(app_config)
    topic_read_pipe = app_config['app_name']+'_wsn'
    MQTT_BROKER = app_config['MQTT_BROKER']
    MQTT_TOPIC = app_config['MQTT_TOPIC']
    mqttc.connect(MQTT_BROKER, 1883)
    threading.Thread(target=pipe_readder, args=(topic_read_pipe, )).start()
    threading.Thread(target=pubb, args=(MQTT_TOPIC, ))

