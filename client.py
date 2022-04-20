#!/usr/bin/env python
import socket
import threading
import os

HEADER = 8
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!exit"
SERVER = "192.168.1.8"
PORT = 5050
ADDR = (SERVER, PORT)
name = "roshan"


def send(connection, msg):
    msg = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length_msg = str(msg_length).encode(FORMAT)
    send_length_msg += b" " * (HEADER - len(send_length_msg))
    connection.send(send_length_msg)
    connection.send(msg)


def receive(connection):
    while (msg_length:= connection.recv(HEADER).decode(FORMAT)):
        msg_length = int(msg_length)
        msg = connection.recv(msg_length).decode(FORMAT)
        print(msg)
        try:
            senderName, receivedMessage = msg.split('>')
            os.system(f'''notify-send """Local Chat:{senderName}""" """{receivedMessage} """''')
        except ValueError:
            os.system(f'''notify-send """Local Chat""" """ {msg} """''')


def write(connection):
    while True:
        msg = input()
        send(connection, msg)
        if msg == DISCONNECT_MESSAGE:
            connection.close()
            quit()


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(ADDR)
send(connection, name)

receive_thread = threading.Thread(target=receive, args=(connection,))
receive_thread.start()

write_thread = threading.Thread(target=write, args=(connection,))
write_thread.start()
