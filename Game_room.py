import random
import threading
import socket
import protocol_library
import sqlite3 as sql
from protocol_library import client_commands, server_game_rooms_commands
import json
from player_game import  Player
import sys
import time
import subprocess
import signal
import os

colors = ["firebrick4", "SteelBlue4", "chartreuse4", "yellow4"]
subprocess1 = ""
threads1 = []


class GameRoom (object):
    def __init__(self, leader_name, maximum_players, ip1, port1, session_id):
        self.session_id = session_id
        self.leader_name = leader_name
        self.players = []
        self.maximum_players = int(maximum_players)
        self.current = "waiting"  # "creating"
        self.count_players = 0
        self.ip = ip1
        self.port = port1
        self.is_full = False
        self.server_open = True

    def join_a_player(self, player_name, conn):
        if self.count_players <= self.maximum_players:
            player1 = Player(self.session_id, colors[self.count_players - 1], conn, player_name)
            self.players.append(player1)
        print(self.players)

    def player_exits_the_room(self, conn):
        self.count_players -= 1
        if self.current == "waiting" and self.is_full:
            self.is_full = False
        for index, player in enumerate(self.players):
            if player.conn == conn:
                del self.players[index]
                break

    """def create_lobby(self):
        # self.players.append({self.leader_name})
        self.current = "waiting"""""

    def check_who_is_on(self):
        # if the cubes got 5, so it searches in the tiles that has 5 which player has a settlement or a city on it, then gives the source to him.
        pass

    def start(self):
        try:
            print(f"The server starts in ip: {self.ip}, and port: {self.port}, session_id is: {self.session_id}")
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("meow hi hav")
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while self.server_open:
                if self.count_players == 0:
                    print("Listening for new clients...")
                print("meow meow hav hav 1 1 hav meow")
                client_socket, client_address = server_socket.accept()
                print(f"A new client has conencted! {client_address}")
                print(f"Players: {self.count_players} out of {self.maximum_players}")
                """if self.count_players == 1:
                    self.join_a_player(self.leader_name)
                else:
                    self.join_a_player()"""
                self.count_players += 1
                print("hi meow hav")
                self.handle_client(client_socket)

        except socket.error as e:
            print(e)

    def handle_player_conn(self, conn):
        try:
            while True:
                request = conn.recv(1024).decode()
                if request is None or request == "":
                    raise ConnectionError
                print(f"\n[Client {conn.getpeername()}] {request}")
                status = self.handle_client_cmd(conn, request)
                if status is not None and status == "CLOSING SERVER":
                    raise BaseException
        except ConnectionError or OSError:
            print(f"There was an error with the client {conn.getpeername()}, so the server closed the socket with him")
            self.player_exits_the_room(conn)
            self.send_information_of_players()
        except BaseException:
            print("meow hav meow meow hav hav meow hav")
            sys.exit(0)
            conn.close()
        except ConnectionRefusedError or ConnectionResetError or ConnectionAbortedError:
            pass

    def handle_client(self, conn):
        client_handler = threading.Thread(target=self.handle_player_conn,
                                          args=(conn,))  # the comma is necessary
        client_handler.daemon = True
        client_handler.start()
        threads1.append(client_handler)

    def handle_client_cmd(self, conn, request):
        con = sql.connect("Data_Bases/accounts_database.db")
        cmd, msg = protocol_library.disassemble_message(request)
        cmd_send, msg_send = "", ""
        if cmd == client_commands["join_my_player_cmd"]:
            if not self.is_full and self.current == "waiting":
                print("meow hav meow 2 1 hav")
                self.join_a_player(msg, conn)
                self.send_information_of_players()
                return
            else:  # just in case
                cmd_send = server_game_rooms_commands["join_player_failed_cmd"]
        elif cmd == client_commands["get_players_information_cmd"]:
            cmd_send, msg_send = self.players_information()
        elif cmd == client_commands["start_game_cmd"]:
            self.start_game()
            return
        elif cmd == client_commands["close_lobby_cmd"]:
            print(self.players)
            if self.players[0].conn == conn:
                message = protocol_library.build_message(server_game_rooms_commands["close_lobby_ok_cmd"], "game server closed, switched back to the main server")
                for player in self.players:
                    print(f"[Server] -> [Client {player.conn.getpeername()}] {message}")
                    conn.sendall(message.encode())
                    self.player_exits_the_room(player.conn)
                    player.conn.close()
                for thread in threads1:
                    thread.join()
                print("CLOSING SERVER")
                self.server_open = False
                sys.exit(1)
                return "CLOSING SERVER"
        elif cmd == client_commands["leave_my_player_cmd"]:
            self.player_exits_the_room(conn)
            message = protocol_library.build_message(server_game_rooms_commands["leave_player_ok_cmd"], self.players_information())
            for player in self.players:
                print(f"[Server] -> [Client {player.conn.getpeername()}] {message}")
                conn.sendall(message.encode())
            return
        message = protocol_library.build_message(cmd_send, msg_send)
        print(f"[Server] -> [Client {conn.getpeername()}] {message}")
        conn.sendall(message.encode())

    def players_information(self):
        try:
            list1 = []
            player_name: Player
            for index, player_name in enumerate(self.players):
                if player_name.get_color() != colors[index] and self.current == "waiting":
                    player_name.change_color(colors[index])
                    list1.append((player_name.player_name, player_name.color))
                elif self.current != "waiting" or player_name.get_color() == colors[index]:
                    list1.append((player_name.player_name, player_name.color))
            list1 = json.dumps(list1 if list1 != [] else [(player_name.player_name, player_name.color) for player in self.players])
            return list1
        except Exception as e:
            print(e)

    def start_game(self):
        self.current = "playing"  # starting the game from the waiting room
        for value in self.players:
            conn = value[3]  # conn
            conn.sendall(protocol_library.build_message(server_game_rooms_commands["start_game_ok"]))

    def send_information_of_players(self):
        cmd_send = server_game_rooms_commands["join_player_ok_cmd"]
        msg_send = self.players_information()
        message = protocol_library.build_message(cmd_send, msg_send)
        for player in self.players:
            conn = player.conn
            print(f"[Server] -> [Client {conn.getpeername()}] {message}")
            conn.sendall(message.encode())

if __name__ == "__main__":
    try:
        ip = "0.0.0.0"
        # print("meow hav hav meow meow hav meow hav")
        leader_name, maximum_players, session_id, port = sys.argv[1:]
        print(leader_name, maximum_players, port, ip, session_id)
        print(sys.argv[:])
        time.sleep(0.5)
        game_server1 = GameRoom(leader_name=leader_name, ip1=ip, port1=int(port), maximum_players=maximum_players, session_id=session_id)
        game_server1.start()
        print("meow meow hav hav 123")
    except Exception as e:
        print(e, "meow hav")
        time.sleep(5)
