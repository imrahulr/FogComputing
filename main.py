# main.py

import sys
import subprocess
import json


def start(app_name):
    f = open(app_name+'.txt', 'r')
    app_config = f.read()
    f.close()
    app_config = json.loads(app_config)
    # subprocess.Popen(['python', 'dispatcher.py', app_config['app_name']])
    subprocess.Popen(['python', 'wsn.py', app_config['port'], app_config['app_name']])


if __name__ == '__main__':
    print("main.py started")
    app_name = sys.argv[1]
    start(app_name)