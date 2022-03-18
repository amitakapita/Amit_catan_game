import socket
import sqlite3
import threading
import protocol_library
import sqlite3 as sql
from protocol_library import server_commands, client_commands
import json
import subprocess
import random
import signal
import os
import asyncio
import multiprocessing


# data bases
wait_login = {}
login_dict = {}
game_room_server_lobbies_session_ids_and_ports = {}
in_game_dict = {}


class Server(object):

    def __init__(self, ip1, port1):
        self.ip = ip1
        self.port = port1
        self.count = 0
        self.count_in_lobby_games_rooms = 0


    def start(self):
        try:
            print(f"The server start in ip: {self.ip}, and port: {self.port}")
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while True:
                if self.count == 0:
                    print("Waiting for a new client...")
                client_socket, client_address = server_socket.accept()  # blocks the running of the file
                print(f"A new client has connected! {client_address}")
                wait_login[client_socket] = client_address
                self.count += 1
                print(f"Number of connected clients: {self.count}\nNumber of players in lobby game rooms: {self.count_in_lobby_games_rooms}")
                self.handle_client(client_socket, self.count)
        except socket.error as e:
            print(e)

    def handle_client(self, conn, number_of_clients):
        client_handler = threading.Thread(target=self.handle_client_connection,
                                          args=(conn, number_of_clients,))  # the comma is necessary
        client_handler.daemon = True
        client_handler.start()

    def handle_client_connection(self, conn, number_of_clients):
        try:
            while True:
                request = conn.recv(1024).decode()
                if request is None or request == "":
                    raise ConnectionError
                print(f"\n[Client] {request}")
                # conn.sendall(request.upper().encode())
                self.handle_client_commands(conn, number_of_clients, request)
        except ConnectionError:
            if conn in wait_login.keys():
                conn.close()
                print(f"There was an error with the client {wait_login[conn]}, so the server closed the socket with him")
                del wait_login[conn]
                self.count -= 1
            else:
                conn.close()
                print(f"There was an error with the client {login_dict[conn]}, so the server closed the socket with him")
                del login_dict[conn]
                self.count -= 1
        except OSError:
            self.count -= 1
            return

    def handle_client_commands(self, conn, number_of_clients, request):
        con = sql.connect("Data_Bases/accounts_database.db")
        cmd, msg = protocol_library.disassemble_message(request)
        to_send, msg_to_send = "", ""
        if cmd == client_commands["login_cmd"]:
            if self.check_login(conn, msg, con):
                to_send = server_commands["login_ok_cmd"]
            else:
                to_send = server_commands["login_failed_cmd"]
        elif cmd == client_commands["sign_up_cmd"]:
            to_send = self.register_check(msg, con)
        elif cmd == client_commands["get_profile_cmd"]:
            to_send, msg_to_send = self.profile(conn, con)
        elif cmd == client_commands["logout_cmd"]:
            wait_login[conn] = login_dict[conn][0]  # only the peer name
            del login_dict[conn]
            return
        elif cmd == client_commands["get_lobby_rooms_cmd"]:
            to_send, msg_to_send = self.lobby_rooms()
        elif cmd == client_commands["create_game_room_lobby_cmd"]:
            session_id = str(random.randint(10000, 100000))
            port_server = str(random.randint(10000, 65536))  # ports available - 10000 - 65535
            while conn.connect_ex(("0.0.0.0", int(port_server))) == 0 and (session_id in game_room_server_lobbies_session_ids_and_ports or port_server == self.port):
                # conn.connect_ex() tries to connect but if there is an error it returns an executing code instead of raising an exception
                session_id = str(random.randint(10000, 100000))
                port_server = str(random.randint(10000, 65536))  # ports available - 10000 - 65535
            game_room_server_lobbies_session_ids_and_ports[session_id] = login_dict[conn][1], msg, False, 1, port_server
            print(f"[Server] Server [{session_id}, {port_server}] is opening")
            thread_server_game_room_lobby_menu = threading.Thread(target=self.create_lobby_rooms_games, args=(conn, msg, session_id, port_server))
            thread_server_game_room_lobby_menu.daemon = True
            thread_server_game_room_lobby_menu.start()
            # self.create_lobby_rooms_games(conn, msg, session_id, port_server)
            to_send = server_commands["create_room_game_lobby_ok_cmd"]
            list_of_names = [(login_dict[conn][1]), ("meow hav 1"), ("hav hav 1 meow"), ("meow meow 1 hav")]
            msg_to_send = "127.0.0.1#" + port_server + "#" + session_id + "#" + json.dumps(list_of_names)
            to_send = protocol_library.build_message(to_send, msg_to_send)
            print(f"[Server] -> [{conn.getpeername()}] {to_send}")
            conn.sendall(to_send.encode())
            print(f"{login_dict[conn][0]} has been switched to game room {session_id}")
            in_game_dict[conn] = login_dict[conn], True, conn
            del login_dict[conn]
            conn.close()
            self.count_in_lobby_games_rooms += 1
            return

        to_send = protocol_library.build_message(to_send, msg_to_send)
        print(f"[Server] -> [{conn.getpeername()}] {to_send}")
        conn.sendall(to_send.encode())

    def check_login(self, conn, msg, con):
        """
        checks the login attempt
        :rtype: bool
        :return: True - the login succeeded, False - the login failed
        """
        username_input, password_input = msg.split("#", 1)
        if (not protocol_library.check_username_validability(username_input)) or password_input == "" or password_input is None:
            return False
        cur = con.cursor()
        cur.execute("SELECT * FROM accounts WHERE Username = ? and Password = ?", (username_input, password_input))
        x = cur.fetchall()
        if x:  # in a list of a tuples
            login_dict[conn] = wait_login[conn], username_input
            print("meow and hav")
            del wait_login[conn]
            return True
        return False

    def register_check(self, msg, con):
        """

        :param msg: msg
        :return: SIGN_UP_OK OR SIGN_UP_FAILED with the reason why it has failed
        """
        username, password, confirm_password, email = msg.split("#")
        if password != confirm_password:
            return server_commands["sign_up_failed_cmd"], "The passwords does not match each other"
        cur = con.cursor()
        cur.execute("INSERT INTO accounts (Username, Password, Email, Played_games, Wined_games) values (?, ?, ?, ?, ?)", (username, password, email, 0, 0))
        """list1 = cur.fetchall()
        if username in sorted(list1, key=lambda x: x[0]):
            return server_commands["sign_up_failed_cmd"], "The name is already taken"
        elif email in sorted(list1, key=lambda x: x[1]):
            return server_commands["sign_up_failed_cmd"], "The Email is already used in another account"
        # elif password != confirm_password:
        #    return "SIGN_UP_FAILED", "The password and the confirmed password do not match each other"
        print(f"INSERT INTO accounts(Username, Password, Email) VALUES ('{username}', '{password}', '{email}')")
        cur.execute(f"INSERT INTO accounts('Username', 'Password', 'Email', 'Played_games', 'Wined_games') VALUES ('{username}', '{password}', '{email}', '{0}', '{0}')")"""
        con.commit()
        return server_commands["sign_up_ok_cmd"]

    """def handle_DB(self, query):
        # con = sql.connect("accounts_database.db")
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return cur.fetchall()"""
    def profile(self, conn, con):
        """ takes the values of games_played and win_games and sends them to the client
        to present the profile nemu to the client

        :param conn: client conn
        :return: games_played#win_games
        """
        cur = con.cursor()
        cur.execute(f"SELECT Played_games, Wined_games, Email FROM 'accounts' WHERE Username = '{login_dict[conn][1]}'")
        msg = cur.fetchall()
        return server_commands["get_profile_ok"], f"{msg[0][0]}#{msg[0][1]}#{msg[0][2]}"

    def lobby_rooms(self):
        lobby_rooms = json.dumps(game_room_server_lobbies_session_ids_and_ports)
        print(lobby_rooms)
        return server_commands["get_lr_ok_cmd"], lobby_rooms

    def create_lobby_rooms_games(self, conn, max_players, session_id, port):
        try:
            process = subprocess.run(["python", "Game_room.py", login_dict[conn][1], max_players, session_id, port], creationflags=subprocess.CREATE_NEW_CONSOLE)
            print(f"closing the game room: {session_id}, {port}")
            self.count_in_lobby_games_rooms -= game_room_server_lobbies_session_ids_and_ports[session_id][3]
            del game_room_server_lobbies_session_ids_and_ports[session_id]
        except subprocess.CalledProcessError as e:
            print(e)

if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 23478
    server1 = Server(ip, port)
    server1.start()
