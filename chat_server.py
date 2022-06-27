import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
# Setup socket intention. (socket is both a name of the library and name of function)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# overcome "Address already in use" message
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind socket to port
server_socket.bind((IP, PORT))
# allow listening to client coming in
server_socket.listen()
# create list of sockets for "select" library to keep track of
sockets_list = [server_socket]
clients = {}     # non-iterable
# message for debug purposes
print(f'Listening for connections on {IP}:{PORT}...')

# Allow server to receive messages and disperse them to connected clients
def receive_message(client_socket):
    try:
# read the header
        message_header = client_socket.recv(HEADER_LENGTH)

# handles maintaining header when client makes a normal exit
        if not len(message_header):
            return False
# convert header to a length
        message_length = int(message_header.decode('utf-8').strip)
# get meaningful data
        return {'header': message_header, 'data': client_socket.recv(message_length)}
# if something went wrong like empty message or client excited abruptly
    except:
         return False

# For continuous loop use while loop. Receive messages for all client sockets, send all their messages to client sockets
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
# Iterate over read sockets for readable data
    for notified_socket in read_sockets:
# If notified socket is server socket, then we got a new connection
        if notified_socket == server_socket:
# Get unique client socket and address
            client_socket, client_address = server_socket.accept()
# Store their username
            user = receive_message(client_socket)
# If client exits before making a username move along
            if user is False:
                continue
# append  new client_socket to our list (sockets_list)
            sockets_list.append(client_socket)
# save client's username
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
# reads socket that comes in as message  instead of server
        else:
            message = receive_message(notified_socket)
# check if there is a message
            if message is False:
                print('closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue
# when it's not disconnected, get info
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
# broadcast info out to all connect clients

# iterate over connected clients and boradcast message
            for client_socket in clients:
# Don't send it back to sender
                if client_socket != notified_socket:
# Send user and message (both w/ their headers)
# We are reusing hre message header sent by sender,
# & saved username header sent by user when their connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

# Account for exception/error sockets

# Iterate over sockets with errors
    for notified_socket in exception_sockets:
# Remove from list for socket.socket()
        sockets_list.remove(notified_socket)
# Remove from our list of users
        del clients[notified_socket]

