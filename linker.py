# linker.py

import socket
import threading
import asyncio


global loop, buffer_pipes, client_list
buffer_pipes = {}
client_list = {}


@asyncio.coroutine
def server_init():
    global loop, soc, buffer_pipes, client_list
    soc = socket.socket()
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(('127.0.0.1', 9009))
    soc.setblocking(False)
    soc.listen(30)
    while True:
        c, a = yield from loop.sock_accept(soc)
        msg = yield from loop.sock_recv(c, 1024)
        msg = msg.decode('utf-8').split('//')
        print(msg)
        if msg[1] not in buffer_pipes:
            buffer_pipes[msg[1]] = []
        if msg[0] == 'pub':
            loop.create_task(dump_pipes(c, msg[1]))
        else:
            if msg[0] == 'sub':
                if msg[1] not in client_list:
                    client_list[msg[1]] = []
                    threading.Thread(target=load_pipes, args=(msg[1],)).start()
                client_list[msg[1]].append(c)


@asyncio.coroutine
def dump_pipes(client, topic):
    global loop, buffer_pipes
    while True:
        msg = yield from loop.sock_recv(client, 1024)
        if msg == '':
            break
        buffer_pipes[topic].append(msg)
        print(msg)


def load_pipes(topic):
    print('Started')
    global loop, buffer_pipes
    while True:
        try:
            if len(buffer_pipes[topic]) != 0:
                data = buffer_pipes[topic].pop(0)
                for c in client_list[topic]:
                    loop.sock_sendall(c, data)
        except:
            break


if __name__ == '__main__':
    print("linker.py started")
    global loop
    loop = asyncio.get_event_loop()
    loop.create_task(server_init())
    loop.run_forever()
