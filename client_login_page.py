import protocol_library
import tkinter as tk
import socket
import threading
import time
from protocol_library import client_commands, server_commands

# Constants:
count1 = 1


class Client(object):

    def __init__(self, ip1, port1):
        self.ip = ip1
        self.port = port1
        self.login_try_count = 0
        self.current_lobby = "login"

        self.root = tk.Tk()
        self.root.title("Catan Game")
        self.root.geometry("500x500+30+30")
        self.back_btn = tk.Button(self.root, text="Back", relief="solid", font="Arial 15", background="#c76969")
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        # Labels and Entries
        self.lbl_welcome_message = tk.Label(self.root, text="Welcome to Catan game!", font="Arial 17")
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
        self.enter_password_input = tk.Entry(self.root, font="Arial 13", show="*")
        self.confirm_password_enter = tk.Label(self.root, text="Password confirm: ", font="Arial 13")
        self.confirm_password_input_enter = tk.Entry(self.root, font="Arial 13", show="*")
        self.Email_enter = tk.Label(self.root, text="E-mail address: ", font="Arial 13")
        self.Email_enter_input = tk.Entry(self.root, font="Arial 13")
        self.lbl2_message = tk.Label(self.root)

        # Lobby
        self.lbl1_welcome_message = tk.Label(self.root, font="Arial 35", bg="#2596be")
        self.profile_btn = tk.Button(self.root, text="View my profile", relief="solid", font="Arial 15")
        self.game_rooms_lobby_btn = tk.Button(self.root, text="Game rooms lobby", relief="solid", font="Arial 15")

        # Profile menu
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, background="#2596be", highlightbackground="#2596be")  # root, screen width, screen height
        self.lbl_profile_message = tk.Label(self.root, font="Arial 35", bg="#2596be")
        self.lbl_games_played = tk.Label(self.root, text="Games played: ", font="Arial 16", bg="grey")
        self.lbl_statistics = tk.Label(self.root, text="My statistics", font="Arial 22", bg="grey")
        self.lbl_games_wins = tk.Label(self.root, text="Win Games: ", font="Arial 16", bg="grey")
        self.lbl_account_data = tk.Label(self.root, text="My account data", font="Arial 22", bg="grey")
        self.lbl_email = tk.Label(self.root, text="E-mail: ", font="Arial 16", bg="grey")



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
            self.back_btn["command"] = lambda: self.back_to_the_menu()
            self.profile_btn["command"] = lambda: self.profile_menu(client_socket)

            # packs login
            self.lbl_welcome_message.pack()
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
        if cmd == server_commands["login_ok_cmd"]:
            self.lbl1_message["text"] = "login succeeded"
            print("login succeeded")
            self.login_try_count = 0
            self.open_menu()
            self.Email = self.Email_enter_input.get()
        elif cmd == server_commands["login_failed_cmd"]:
            self.lbl1_message["text"] = f"login failed, you have {2 - self.login_try_count} attempts to login"
            print("login failed")
            self.login_try_count += 1
            if self.login_try_count == 3:
                self.submit_btn["state"] = tk.DISABLED
                self.name1_input["state"] = tk.DISABLED
                self.password1_input["state"] = tk.DISABLED
        elif cmd == server_commands["sign_up_ok_cmd"]:
            # self.register_btn["state"] = tk.DISABLED
            self.lbl2_message["text"] = "Register succeeded"
            time.sleep(2)
            self.not_in_register_menu()
            self.login_menu()
        elif cmd == server_commands["sign_up_failed"]:
            self.lbl2_message["text"] = msg
        elif cmd == server_commands["get_profile_ok"]:
            games_played, games_win = msg.split("#")
            self.lbl_games_played["text"] += games_played
            self.lbl_games_wins["text"] += games_win

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
            data, msg = client_commands["login_cmd"], "%s#%s" % (self.username, self.password)
            self.send_messages(conn, data, msg)

    def open_menu(self):
        self.not_in_login_menu()
        self.current_lobby = "main_lobby"

        self.root.title(f"{self.username}'s Catan main lobby")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#2596be")
        self.lbl1_welcome_message["text"] = f"Welcome {self.username} to the main lobby!"
        self.lbl1_welcome_message.pack(side=tk.TOP)
        self.back_btn.place(x=1200, y=15)
        self.profile_btn.place(x=350, y=500)
        self.game_rooms_lobby_btn.place(x=850, y=500)

    def register_menu(self):
        self.current_lobby = "register"
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
        self.back_btn.pack()

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
        elif self.password != self.confirmed_password:
            self.lbl2_message["text"] = "the password does not match the confirmed password"
        else:
            data, msg = client_commands["sign_up_cmd"], "{}#{}#{}#{}".format(self.username, self.password, self.confirmed_password,
                                                        self.Email)
            self.send_messages(conn, data, msg)

    def not_in_login_menu(self):
        self.name1.pack_forget()
        self.name1_input.pack_forget()
        self.password1.pack_forget()
        self.password1_input.pack_forget()
        self.submit_btn.pack_forget()
        self.lbl1_message.pack_forget()
        self.register_btn.pack_forget()
        self.lbl_welcome_message.pack_forget()

    def not_in_register_menu(self):
        self.title.pack_forget()
        self.enter_name.pack_forget()
        self.enter_name_input.pack_forget()
        self.enter_password.pack_forget()
        self.enter_password_input.pack_forget()
        self.confirm_password_enter.pack_forget()
        self.confirm_password_input_enter.pack_forget()
        self.Email_enter.pack_forget()
        self.Email_enter_input.pack_forget()
        self.lbl2_message.pack_forget()
        self.register_account_btn.pack_forget()
        self.back_btn.pack_forget()

    def login_menu(self):
        self.root.title("Catan Game")
        if self.current_lobby == "main_lobby":
            self.root.attributes("-fullscreen", False)
            self.root.configure(bg="#f0f0f0")
        # packs login
        self.lbl_welcome_message.pack()
        self.name1.pack()
        self.name1_input.pack()
        self.password1.pack()
        self.password1_input.pack()
        self.submit_btn.pack()
        self.lbl1_message.pack()
        self.register_btn.pack()

    def back_to_the_menu(self):
        if self.current_lobby == "register":
            self.not_in_register_menu()
            self.login_menu()
        elif self.current_lobby == "main_lobby":
            self.not_in_main_lobby()
            self.login_menu()
        elif self.current_lobby == "profile":
            self.not_in_profile_menu()
            self.open_menu()

    def not_in_main_lobby(self):
        self.lbl1_welcome_message.pack_forget()
        if self.current_lobby != "profile":
            self.back_btn.place_forget()
        self.profile_btn.place_forget()
        self.game_rooms_lobby_btn.place_forget()

    def profile_menu(self, conn):
        self.current_lobby = "profile"
        self.not_in_main_lobby()
        self.lbl_profile_message["text"] = f"{self.username}'s Profile"
        self.lbl_profile_message.pack(side=tk.TOP)
        self.canvas.pack()
        self.canvas.create_rectangle(70, 50, 550, 400, fill="grey", outline="black")
        self.lbl_statistics.place(x=220, y=122)
        self.lbl_games_played.place(x=80, y=200)
        self.lbl_games_wins.place(x=80, y=300)
        self.canvas.create_rectangle(700, 50, 1200, 300, fill="grey", outline="black")
        self.lbl_account_data.place(x=850, y=122)
        self.lbl_email["text"] += self.Email
        self.lbl_email.place(x=710, y=200)
        self.send_messages(conn, client_commands["get_profile_cmd"])

    def not_in_profile_menu(self):
        self.canvas.pack_forget()
        self.lbl_profile_message.pack_forget()
        self.lbl_statistics.place_forget()
        self.lbl_games_played.place_forget()
        self.lbl_games_wins.place_forget()
        self.lbl_account_data.place_forget()
        self.lbl_email.place_forget()



if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 23478
    client1 = Client(ip, port)
    client1.start()
