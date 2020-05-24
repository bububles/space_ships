import socket
import pickle
import pygame
from _thread import *
from player import Player

pygame.init()
server = "127.0.0.1"
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server, port))
s.listen(2)
print("Waiting for a connection, Server Started")

color1 = (255, 255, 0)
color2 = (0, 225, 255)
player1 = Player(200-11, 20, color1)
player2 = Player(200-11, 400-20-23, color2)
players = [player1, player2]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
