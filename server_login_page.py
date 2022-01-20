import socket
import sqlite3
import threading
import protocol_library
import sqlite3 as sql


# data bases
wait_login = {}


class Server(object):

    def __init__(self, ip1, port1):
        self.ip = ip1
        self.port = port1
        self.count = 0


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
                print(f"Number of connected clients: {self.count}")
                self.handle_client(client_socket, self.count)
        except socket.error as e:
            print(e)

    def handle_client(self, conn, number_of_clients):
        client_handler = threading.Thread(target=self.handle_client_connection,
                                          args=(conn, number_of_clients,))  # the comma is necessary
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
            print(f"There was an error with the client {wait_login[conn]}, so the server closed the socket with him")
            del wait_login[conn]
            self.count -= 1

    def handle_client_commands(self, conn, number_of_clients, request):
        con = sql.connect("Data_Bases/accounts_database.db")
        cmd, msg = protocol_library.disassemble_message(request)
        to_send = ""
        if cmd == "LOGIN":
            if self.check_login(conn, msg, con):
                to_send = "LOGIN_OK"
            else:
                to_send = "LOGIN_FAILED"
        elif cmd == "SIGN_UP":
            to_send = self.register_check(msg, con)
        to_send = protocol_library.build_message(to_send)
        print(f"[Server] -> [{wait_login[conn]}] {to_send}")
        conn.sendall(to_send.encode())

    def check_login(self, conn, msg, con):
        """
        checks the login attempt
        :rtype: bool
        :return: True - the login succeeded, False - the login failed
        """

        username_input, password_input = msg.split("#")

        cur = con.cursor()
        cur.execute("SELECT Username, Password FROM accounts")
        x = cur.fetchall()
        print(x)
        if (username_input, password_input) in x:  # in a list of a tuples
            return True
        return False

    def register_check(self, msg, con):
        """

        :param msg: msg
        :return: SIGN_UP_OK OR SIGN_UP_FAILED with the reason why it has failed
        """
        username, password, confirm_password, email = msg.split("#")
        cur = con.cursor()
        cur.execute("SELECT Username, Email FROM accounts")
        list1 = cur.fetchall()
        if username in sorted(list1, key=lambda x: x[0]):
            return "SIGN_UP_FAILED", "The name is already taken"
        elif email in sorted(list1, key=lambda x: x[1]):
            return "SIGN_UP_FAILED", "The Email is already used in another account"
        # elif password != confirm_password:
        #    return "SIGN_UP_FAILED", "The password and the confirmed password do not match each other"
        print(f"INSERT INTO accounts(Username, Password, Email) VALUES ('{username}', '{password}', '{email}')")
        cur.execute(f"INSERT INTO accounts('Username', 'Password', 'Email') VALUES ('{username}', '{password}', '{email}')")
        con.commit()
        return "SIGN_UP_OK"

    """def handle_DB(self, query):
        # con = sql.connect("accounts_database.db")
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return cur.fetchall()"""

if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 23478
    server1 = Server(ip, port)
    server1.start()
