# import socket
# import time
# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serv.bind(('127.0.0.1', 4040))
# serv.listen(5)
#
# while True:
#     conn, addr = serv.accept()
#     while True:
#         data = conn.recv(4096)
#         if not data: break
#
#         value = data.decode('utf8')
#         if(value != "RECEIVED"): print(f'From client: {value}')
#
#         conn.send("Hello!".encode())
#         time.sleep(4)
#     conn.close()
#
# print('client disconnected and shutdown')
# !/usr/bin/python           # This is server.py file

import socket  # Import socket module
import threading
import time


unreadMessageParty1 = []
unreadMessageParty2 = []

def on_new_client(conn, addr, number):
    while True:
        data = conn.recv(4096)
        if not data: break

        value = data.decode('utf8')
        if (value != "RECEIVED"):
            print(f'From client: {value}')
            if(number == 0):
                unreadMessageParty2.append(value)
            if(number == 1):
                unreadMessageParty1.append(value)

        if(number == 0):
            if(len(unreadMessageParty1) > 0):
                message = unreadMessageParty1.pop()
                conn.send(message.encode())
        if(number == 1):
            if(len(unreadMessageParty2) > 0):
                message = unreadMessageParty2.pop()
                conn.send(message.encode())
        # time.sleep(0.01)
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
server.bind(('127.0.0.1', 4040))

print('Server started!')
print('Waiting for clients...')

server.listen(5)  # Now wait for client connection.

activeThreads = []

while True:
    conn, addr = server.accept()  # Establish connection with client.
    thread = threading.Thread(target=(lambda: on_new_client(conn, addr, len(activeThreads))))
    thread.start()
    activeThreads.append(thread)


s.close()
