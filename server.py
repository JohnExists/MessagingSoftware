import socket  # Import socket module
import threading

unreadMessageParty1 = []
unreadMessageParty2 = []

def on_new_client(conn, number):
    while True:
        data = conn.recv(4096)
        if not data: break

        value = data.decode('utf8')
        if (value != "RECEIVED"):
            print(f'From client {number}: {value}')
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
    unreadMessageParty1.clear()
    unreadMessageParty2.clear()
    activeThreads.clear()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
server.bind(('127.0.0.1', 4040))

print('Server started!')
print('Waiting for clients...')

server.listen(5)  # Now wait for client connection.

activeThreads = []

while True:
    conn, addr = server.accept()  # Establish connection with client.
    thread = threading.Thread(target=(lambda: on_new_client(conn, len(activeThreads))))
    thread.start()
    activeThreads.append(thread)


s.close()
