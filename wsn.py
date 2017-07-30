# wsn.py

import socket
import sys
import pipes
import asyncio
import threading
import time


global app_name, loop, soc, client_list, pipe_pub_topic, pipe_sub_topic


@asyncio.coroutine
def server_init(address):
    global soc, loop
    soc = socket.socket()
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((address))
    #soc.setblocking(False)
    soc.setblocking(True)
    soc.listen(30)
    print("Listening...." + str(address))
    while True:
        c, a = yield from loop.sock_accept(soc)
        print("Connected with"+str(a))
        msg = yield from loop.sock_recv(c, 32)
        msg = msg.decode('utf-8').split(':')
        if msg[0] == 'pub':
            loop.create_task(read_client(c))
        elif msg[0] == 'sub':
            if msg[1] not in client_list:
                client_list[msg[1]] = []
                threading.Thread(target=write_clients, args=(msg[1])).start()
            client_list[msg[1]].append(c)


@asyncio.coroutine
def read_client(client):
    p = pipes.pipes('pub', pipe_pub_topic)
    while True:
        data = yield from loop.sock_recv(client, 32)
        data = data.decode('utf-8')
        print(data)
        if data == '':
            print('Break')
            break
        p.write_pipes(data)


def write_clients(topic):
    pipe_sub_topic = app_name+'_'+topic
    p = pipes.pipes('sub', pipe_sub_topic)
    while True:
        data = p.read_pipes()
        for c in client_list[topic]:
            try:
                loop.sock_sendall(c, data)
            except:
                pass


if __name__ == '__main__':
    print("wsn.py started")
    global app_name, loop, pipe_pub_topic, pipe_sub_topic
    port = int(sys.argv[1])
    app_name = sys.argv[2]
    pipe_pub_topic = app_name+'_wsn'
    loop = asyncio.get_event_loop()
    loop.create_task(server_init(('', port)))
    loop.run_forever()