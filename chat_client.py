import socket
import select
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username:")

# Setup socket intention. (socket is both a name of the library and name of function)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# have socket able to connect
client_socket.connect((IP, PORT))
# set receive block to off
client_socket.setblocking(False)

# set up username as 1st message that server will receive
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
# send username to server
client_socket.send(username_header + username)


# Accept new messages from client
while True:
# using input function will block rest of code from running/updating messages
# so we will need to send a message to see the updates
    message = input(f'{my_username} > ')
# check if there is a message
    if message:
# encode message to bytes, prepare header & convert to bytes,
# like username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
# send message
        client_socket.send(message_header + message)

# indefinitely attempt to receive messages
    try:
        while True:
# accept server socket
            username_header = client_socket.recv(HEADER_LENGTH)
# If we received no data, server gracefully closed a connection, for example using socket.close()
# or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
# Actual getting username
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
# get messages
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
# Output message to screen
            print(f'{username} > {message}')

# accepting errors resulting from no longer receiving messages
    except IOError as e:
# This is normal on non blocking connections - when there are no incoming data error is going to be raised
# Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
# We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
# If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
# Not receiving data
        continue
# Any other exception - something happened, exit
    except Exception as e:
        print ('Reading error: '.format(str(e)))
        sys.exit()





