# fog.py

import subprocess
import os
import paho.mqtt.client as mqtt
import json


global mqttc, serv_topic, fog_topic
serv_topic = 'server'
fog_topic = 'fog'


def on_connect(mosq, obj, rc):
    global mqttc
    mqttc.subscribe((fog_topic, 0))


def on_message(mosq, obj, msg):
    msg = msg.payload.decode('utf-8')
    msg = json.loads(msg)
    print(msg)
    f = open('config/'+msg['app_name']+'.txt', 'w')
    f.write(json.dumps(msg))
    f.close()
    subprocess.Popen(['python3', 'main.py', msg['app_name']])


# for sending messages to the server
def pub(msg):
    global mqttc, serv_topic
    mqttc.publish(serv_topic, msg.encode('utf-8'))


if __name__ == '__main__':
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect('127.0.0.1', 1883)
    subprocess.Popen(['python', 'linker.py'])
    f = os.listdir('config')
    df = {}
    for i in f:
        print(i)
        f = open('config/'+i, 'r')
        df = json.loads(f.read())
        print(df)
        subprocess.Popen(['python', 'main.py', df['app_name']])
    while True:
        mqttc.loop_start()