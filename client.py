# client.py

import asyncio
import socket


def client():
    s = socket.socket()
    address = "192.168.1.101", 9009
    s.connect(address)
    data = "pub:data"
    s.send(data.encode('utf-8'))
    print(data)


if __name__ == '__main__':
    print("client.py started")
    #loop = asyncio.get_event_loop()
    #loop.create_task(client_init())
    #loop.run_forever()
    client()