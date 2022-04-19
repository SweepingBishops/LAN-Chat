#!/usr/bin/env python
import socket
import threading

###GLOBAL CONSTANTS###
HEADER = 8
PORT = 5050
SERVER = "192.168.1.5"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

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
    print(f"{name} has connected.")
    for client in clients:
        if client != connection:
            send(client, f"[{name} has connected.]")

    connected = True
    while connected:
        msg = receive(connection)

        if msg == DISCONNECT_MESSAGE:
            for client in clients:
                if client != connection:
                    send(client, f"[{name} has disconnected.]")
            connection.close()
            print(f"{name} has disconnected.")
            clients.remove(connection)
            connected = False
            break

        print(f"{name}> {msg}")
        for client in clients:
            if client != connection:
                send(client, f"{name}> {msg}")
        continue


def start_server():
    server.listen()
    print(f"[INFO] Starting server on:{SERVER}, listening on port:{PORT}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()


start_server()
