import socket  # Import socket module
import threading

# The unread messages for each party
unreadMessageParty1 = []
unreadMessageParty2 = []

def on_new_client(conn, number):
    while True:
        data = conn.recv(4096)
        if not data: break

        value = data.decode('utf8')
        # If the server received a proper message from the client
        if (value != "RECEIVED"):
            print(f'From client {number}: {value}')
            # Send that message to the other party
            if(number == 0): unreadMessageParty2.append(value)
            if(number == 1): unreadMessageParty1.append(value)

        # Send any unread messages to the client
        if(number == 0):
            if(len(unreadMessageParty1) > 0):
                message = unreadMessageParty1.pop()
                conn.send(message.encode())
        if(number == 1):
            if(len(unreadMessageParty2) > 0):
                message = unreadMessageParty2.pop()
                conn.send(message.encode())
    conn.close()
    unreadMessageParty1.clear()
    unreadMessageParty2.clear()
    activeThreads.clear()

# Initialize the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
server.bind(('127.0.0.1', 4040))

print('Server started!')
print('Waiting for clients...')

server.listen(5)  # Now wait for client connection.

activeThreads = []

# Checks for all the clients that connected
while True:
    conn, addr = server.accept()  # Establish connection with client.
    thread = threading.Thread(target=(lambda: on_new_client(conn, len(activeThreads))))
    thread.start()
    activeThreads.append(thread)


s.close()
