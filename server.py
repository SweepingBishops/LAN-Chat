#!/usr/bin/env python
import socket
import threading
from sys import platform
from os import system

###GLOBAL CONSTANTS###
SYSTEM = platform
HEADER = 8
# ip a|grep 'state UP' -A2|tail -n1|awk '{print $2}'|cut -f1 -d'/'
if SYSTEM == "linux":
    SERVER = str(system("ip a|grep 'state UP' -A2|tail -n1|awk '{print $2}'|cut -f1 -d'/'"))
elif SYSTEM == "osx":
    SERVER = str(system("ifconfig | grep 'inet ' | grep -Fv 127.0.0.1 | awk '{print $2}'"))  # To be tested.
PORT = 55555
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!exit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDRESS)
except OSError as e:
    print(e)
    quit()

clients = []


def send(connection, msg):
    msg = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length_msg = str(msg_length).encode(FORMAT)
    send_length_msg += b" " * (HEADER - len(send_length_msg))
    connection.send(send_length_msg)
    connection.send(msg)


def receive(connection):
    msg_length = connection.recv(HEADER).decode(FORMAT)
    if not msg_length:
        return
    msg_length = int(msg_length)
    msg = connection.recv(msg_length).decode(FORMAT)
    return msg


def handle_client(connection):
    clients.append(connection)
    name = receive(connection)
    if '"' in name or "'" in name:
        send(connection, "Names cannot contain quotes.")
        connection.close()
        return
    send(connection, "Successfully connected to server! Type '!exit' to disconnect.")
    for client in clients:
        if client != connection:
            send(client, f"[{name} has connected.]")

    connected = True
    while connected:
        msg = receive(connection)

        if msg == DISCONNECT_MESSAGE or msg is None:
            for client in clients:
                if client != connection:
                    send(client, f"[{name} has disconnected.]")
            connection.close()
            clients.remove(connection)
            connected = False
            break

        for client in clients:
            if client != connection:
                send(client, f"{name}> {msg}")


def start_server():
    server.listen()
    print(f"[INFO] Starting server on:{SERVER}, listening on port:{PORT}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()


start_server()
