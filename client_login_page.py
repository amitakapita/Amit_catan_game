import protocol_library
import tkinter as tk
import socket
import threading

# Constants:
count1 = 1


class Client(object):

    def __init__(self, ip1, port1):
        self.ip = ip1
        self.port = port1
        self.login_try_count = 0

        self.root = tk.Tk()
        self.root.title("Catan Game")
        self.root.geometry("500x500+30+30")

        # Labels and Entries
        self.name1 = tk.Label(self.root, text="Username: ")
        self.name1_input = tk.Entry(self.root, font="Arial 13")
        self.password1 = tk.Label(self.root, text="Password: ")
        self.password1_input = tk.Entry(self.root, font="Arial 13", show="*")
        self.submit_btn = tk.Button(self.root, text="Login", relief="solid")
        self.lbl1_message = tk.Label(self.root)
        self.register_btn = tk.Button(self.root, text="Register", relief="solid")


        self.username = ""
        self.password = ""
        self.confirmed_password = ""
        self.Email = ""

        # Register menu
        self.title = tk.Label(self.root, text="Register an account", font="Arial 15")
        self.register_account_btn = tk.Button(self.root, text="Register", relief="solid")
        self.enter_name = tk.Label(self.root, text="New Username: ", font="Arial 13")
        self.enter_name_input = tk.Entry(self.root, font="Arial 13")
        self.enter_password = tk.Label(self.root, text="Password: ", font="Arial 13")
        self.enter_password_input = tk.Entry(self.root, font="Arial 13")
        self.confirm_password_enter = tk.Label(self.root, text="Password confirm: ", font="Arial 13")
        self.confirm_password_input_enter = tk.Entry(self.root, font="Arial 13")
        self.Email_enter = tk.Label(self.root, text="E-mail address: ", font="Arial 13")
        self.Email_enter_input = tk.Entry(self.root, font="Arial 13")
        self.lbl2_message = tk.Label(self.root)


    def start(self):
        try:
            print("meow")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, self.port))

            # send_connection_thread = threading.Thread(target=self.send_messages, args=(client_socket,))
            # send_connection_thread.start()
            receive_connection_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            receive_connection_thread.daemon = True
            receive_connection_thread.start()
            # while True:
            # data = client_socket.recv(1024).decode()
            self.submit_btn["command"] = lambda: self.check_in(client_socket)
            self.register_btn["command"] = lambda: self.register_menu()
            self.register_account_btn["command"] = lambda: self.register_account(client_socket)

            # packs login
            self.name1.pack()
            self.name1_input.pack()
            self.password1.pack()
            self.password1_input.pack()
            self.submit_btn.pack()
            self.lbl1_message.pack()
            self.register_btn.pack()

            self.root.mainloop()

        except socket.error as e:
            print(e)

    def receive_messages(self, conn):
        while True:
            data = conn.recv(1024).decode()
            self.handle_received_connection(conn, data)

    def send_messages(self, conn, data, msg=""):
        while True:
            message = protocol_library.build_message(data, msg)
            print(f"[Client] {message}")
            conn.sendall(message.encode())
            break

    def handle_received_connection(self, conn, data):
        print(f"[Server] {data}")
        cmd, msg = protocol_library.disassemble_message(data)
        if cmd == "LOGIN_OK":
            self.lbl1_message["text"] = "login succeeded"
            print("login succeeded")
            self.login_try_count = 0
            self.open_menu()
        elif cmd == "LOGIN_FAILED":
            self.lbl1_message["text"] = f"login failed, you have {2-self.login_try_count} attempts to login"
            print("login failed")
            self.login_try_count += 1
            if self.login_try_count == 3:
                self.submit_btn["state"] = tk.DISABLED
                self.name1_input["state"] = tk.DISABLED
                self.password1_input["state"] = tk.DISABLED

    def check_in(self, conn):
        self.username, self.password = (self.name1_input.get(), self.password1_input.get())
        print(self.password)
        if self.username == "":
            self.lbl1_message["text"] = "the username isn't empty"
            print("the username isn't empty")
        elif self.password == "":
            self.lbl1_message["text"] = "the password isn't empty"
            print("the password isn't empty")
        else:
            data, msg = "LOGIN", "%s#%s" % (self.username, self.password)
            self.send_messages(conn, data, msg)

    def open_menu(self):
        self.not_in_login_menu()

        self.root.title(f"{self.username}'s Catan lobby")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#2596be")

    def register_menu(self):
        self.not_in_login_menu()

        self.root.title("Register an account")
        self.title.pack()
        self.enter_name.pack()
        self.enter_name_input.pack()
        self.enter_password.pack()
        self.enter_password_input.pack()
        self.confirm_password_enter.pack()
        self.confirm_password_input_enter.pack()
        self.Email_enter.pack()
        self.Email_enter_input.pack()
        self.lbl2_message.pack()
        self.register_account_btn.pack()


    def not_in_login_menu(self):
        self.name1.destroy()
        self.name1_input.destroy()
        self.password1.destroy()
        self.password1_input.destroy()
        self.submit_btn.destroy()
        self.lbl1_message.destroy()
        self.register_btn.destroy()

    def register_account(self, conn):
        self.username, self.password, self.confirmed_password, self.Email = self.enter_name_input.get(), self.enter_password_input.get(), self.confirm_password_input_enter.get(), self.Email_enter_input.get()
        if self.username == "":
            self.lbl2_message["text"] = "the username isn't empty"
        elif self.password == "":
            self.lbl2_message["text"] = "the password isn't empty"
        elif self.confirmed_password == "":
            self.lbl2_message["text"] = "the confirmed password isn't empty"
        elif self.Email == "":
            self.lbl2_message["text"] = "the email isn't empty"
        else:
            data, msg = "SIGN_UP", "{}#{}#{}#{}".format(self.username, self.password, self.confirmed_password, self.Email)
            self.send_messages(conn, data, msg)




if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 23478
    client1 = Client(ip, port)
    client1.start()
