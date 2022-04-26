import protocol_library
import tkinter as tk
import socket
import threading
import time
from protocol_library import client_commands, server_commands, server_game_rooms_commands
import json
from PIL import ImageTk, Image
import PIL
from some_from_hex_tile import *
import typing
from typing import Type
import traceback
from types import SimpleNamespace

# Constants:
count1 = 1
colors = ["firebrick4", "SteelBlue4", "chartreuse4", "#DBB600"]
dict_colors = {"firebrick4": "red", "SteelBlue4": "blue", "chartreuse4": "green", "#DBB600": "yellow"}
dict_colors1 = {"red": "firebrick4", "blue": "SteelBlue4", "green": "chartreuse4", "yellow": "#DBB600"}


class Client(object):

    def __init__(self, ip1, port1):
        self.ip = ip1
        self.port = port1
        self.login_try_count = 0
        self.current_lobby = "login"

        self.ip2 = ""
        self.port2 = 0
        self.second_time_connect = False
        self.main_server = True

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

        # Game rooms lobby menu
        self.scrollbar_frame = tk.Frame(self.root, highlightbackground="black", highlightcolor="black", highlightthickness=2, bg="#2596be")
        self.scrollbar = tk.Scrollbar(self.scrollbar_frame, orient=tk.VERTICAL)
        self.game_rooms_lobby_lbl = tk.Label(self.root, font="Arial 35", bg="#2596be", text="Game rooms lobby")
        self.games_rooms_list = tk.Listbox(self.scrollbar_frame, font="Arial 40", bg="#2596be", width=26, relief="flat", highlightbackground="black", height=9, highlightcolor="black")
        # self.games_rooms_list.insert(1, game_room1)  # add an id and a game_room object
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.games_rooms_list.insert(1, "meow")
        self.game_rooms_lobby_canvas = tk.Canvas(self.scrollbar_frame, bg="#2596be", highlightbackground="#2596be", highlightcolor="#2596be", highlightthickness=2, height=900, width=755)
        self.game_rooms_lobby_canvas.configure(scrollregion=(300, 150, 900, 700))
        self.game_rooms_lobby_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.refresh_button = tk.Button(self.root, bg="#70ad47", text="Refresh", relief="solid", font="Arial 18")
        self.create_lobby_game_room_button = tk.Button(self.root, bg="#70ad47", text="Create", relief="solid", font="Arial 18")
        self.from_creating = False
        self.from_main_lobby = False
        self.is_active = False
        self.from_lobby_game_waiting_or_in_actual_game = False
        self.message_failed_join_error_game = tk.Label(self.root, bg="#2596be", font="Arial 16")

        # create lobby room menu
        self.lobby_name_game_room_lbl = tk.Label(self.root, font="Arial 30", bg="#2596be")
        self.game_room_lobby_create_canvas = tk.Canvas(self.root, bg="#d0cece", width=700, height=300, highlightcolor="black", highlightbackground="black")
        self.maximum_players_entry = tk.Entry(self.root, bg="#AFABAB", font="Arial 20")
        self.maximum_players_lbl = tk.Label(self.root, bg="#d0cece", font="Arial 20", text="Maximum participants: {2-4}")
        self.create_lobby_game_room_create_button = tk.Button(self.root, bg="#70ad47", text="Create lobby", font="Arial 15", relief="solid")
        self.number_players_not_valid = tk.Label(self.root, bg="#d0cece", font="Arial 15", text="The maximum players should be between 2 (include 2) to 4 (include 4)")

        # waiting lobby room menu
        self.waiting_to_start_lbl = tk.Label(self.root, bg="#2596be", font="Arial 15")
        self.waiting_room_lobby_menu_canvas = tk.Canvas(self.root, bg="#d0cece", width=900, height=400, highlightcolor="black", highlightbackground="black")
        self.start_game_menu_button = tk.Button(self.root, bg="#70ad47", text="Start", font="Arial 15", relief="solid")
        self.session_id_lbl = tk.Label(self.root, bg="#d0cece", font="Arial 15")
        self.participants_lbl = tk.Label(self.root, bg="#d0cece", font="Arial 17")
        self.name_leader = tk.Label(self.root, bg="#2596be", font="Arial 30")
        self.list_of_players = []

        # playing room
        self.canvas_game = tk.Canvas(self.root, bg="#2596be", width=900, highlightbackground="black", highlightthickness=3)
        self.tiles = []
        self.ports = []

        self.Circle_choosing_image_path = r"assets\Circle_choosing1.png"
        self.Circle_choosing_photo_image = Image.open(self.Circle_choosing_image_path).convert("RGBA")
        self.Circle_choosing_photo_image = ImageTk.PhotoImage(self.Circle_choosing_photo_image)
        self.none_any_circle = ImageTk.PhotoImage(Image.open(r"assets\None_of_circles.png").convert("RGBA"))
        self.ids_placements = []
        self.current_button = None
        self.button_buy_road = tk.Button(self.root, text="Buy Road", relief="solid", font="Arial 15", bg="SkyBlue3",
                                         activebackground="SkyBlue2",
                                         command=lambda: self.change_current_button("road"), state=tk.DISABLED)
        self.button_buy_boat = tk.Button(self.root, text="Buy Boat", relief="solid", font="Arial 15", bg="SkyBlue3",
                                         activebackground="SkyBlue2",
                                         command=lambda: self.change_current_button("boat"), state=tk.DISABLED)
        self.button_buy_settlement = tk.Button(self.root, text="Buy Settlement", relief="solid", font="Arial 15",
                                               bg="SkyBlue3",
                                               activebackground="SkyBlue2",
                                               command=lambda: self.change_current_button("settlement"), state=tk.DISABLED)
        self.button_buy_city = tk.Button(self.root, text="Buy City", relief="solid", font="Arial 15", bg="SkyBlue3",
                                         activebackground="SkyBlue2",
                                         command=lambda: self.change_current_button("city"), state=tk.DISABLED)
        self.button_buy_development_card = tk.Button(self.root, text="Buy Development Card", relief="solid", font="Arial 15",
                                                     bg="SkyBlue3", activebackground="SkyBlue2",
                                                     command=lambda: self.change_current_button("development_card"), state=tk.DISABLED)
        self.button_declare_victory = tk.Button(self.root, text="Declare Victory", relief="solid", font="Arial 15",
                                                bg="SkyBlue3",
                                                activebackground="SkyBlue2",
                                                command=lambda: self.change_current_button("declare_victory"), state=tk.DISABLED)
        self.button_next_turn = tk.Button(self.root, text="Finished My Turn", relief="solid", font="Arial 15", bg="SkyBlue3",
                                          activebackground="SkyBlue2",
                                          command=lambda: self.change_current_button("next_turn"), state=tk.DISABLED)
        self.where_place = tk.Label(self.root, text="Where to place?", bg="#2596be", font="Arial 15")
        self.place_entry = tk.Entry(self.root, bg="SkyBlue3", font="Arial 15")
        self.button_buy = tk.Button(self.root, bg="SkyBlue3", activebackground="SkyBlue2", font="Arial 15", text="Buy", relief="solid")
        self.image1 = Image.open(r"assets\Settlement_red.png").convert("RGBA")
        self.image1 = ImageTk.PhotoImage(self.image1)
        self.image2 = ImageTk.PhotoImage(Image.open(r"assets\Settlement_blue.png").convert("RGBA"))
        self.image3 = ImageTk.PhotoImage(Image.open(r"assets\Settlement_green.png").convert("RGBA"))
        self.image4 = ImageTk.PhotoImage(Image.open(r"assets\Settlement_yellow.png").convert("RGBA"))
        self.settlements = []  # (index, settlement)
        self.cities = []  # (index, city)
        self.image_city_red = ImageTk.PhotoImage(Image.open(r"assets/City_red.png").convert("RGBA"))
        self.image_city_blue = ImageTk.PhotoImage(Image.open(r"assets/City_blue.png").convert("RGBA"))
        self.image_city_green = ImageTk.PhotoImage(Image.open(r"assets/City_green.png").convert("RGBA"))
        self.image_city_yellow = ImageTk.PhotoImage(Image.open(r"assets/City_yellow.png").convert("RGBA"))
        self.roads = []
        self.cancel_buying_button = tk.Button(self.root, bg="SkyBlue3", activebackground="SkyBlue2", font="Arial 15", text="Cancel", relief="solid", command=self.close_placements)
        self.boats = []
        self.image_path_boat1 = fr"assets\Boat_red.png"
        self.image_boat_1 = ImageTk.PhotoImage(Image.open(self.image_path_boat1).convert("RGBA"))
        self.image_boat_2 = ImageTk.PhotoImage(Image.open(fr"assets\Boat_blue.png").convert("RGBA"))
        self.image_boat_3 = ImageTk.PhotoImage(Image.open(fr"assets\Boat_green.png").convert("RGBA"))
        self.image_boat_4 = ImageTk.PhotoImage(Image.open(fr"assets\Boat_yellow.png").convert("RGBA"))
        self.button_pull_cubes = tk.Button(self.root, relief="solid", bg="SkyBlue3", activebackground="SkyBlue2", font="Arial 15", text="pull cubes", state=tk.DISABLED)
        self.lbl_cube1 = tk.Label(self.root, bg="#2596be")
        self.lbl_cube2 = tk.Label(self.root, bg="#2596be")
        self.cubes_images = [ImageTk.PhotoImage(Image.open(fr"assets\cube_1.png").convert("RGBA")), ImageTk.PhotoImage(Image.open(fr"assets\cube_2.png").convert("RGBA")),
                      ImageTk.PhotoImage(Image.open(fr"assets\cube_3.png").convert("RGBA")), ImageTk.PhotoImage(Image.open(fr"assets\cube_4.png").convert("RGBA")),
                      ImageTk.PhotoImage(Image.open(fr"assets\cube_5.png").convert("RGBA")), ImageTk.PhotoImage(Image.open(fr"assets\cube_6.png").convert("RGBA"))]
        self.sum_cubes_lbl = tk.Label(self.root, bg="#2596be", font="Arial 15")
        self.bytes_times_counter = 0
        self.map_storage = None
        self.tiles_images = []
        self.place_numbers_path = r"assets\place_numbers.png"
        self.place_numbers_image = Image.open(place_numbers_path).convert("RGBA")
        self.numbers_path = r"assets\numbers2.png"
        self.numbers1_image = Image.open(numbers_path).convert("RGBA")
        self.place_numbers_image = ImageTk.PhotoImage(self.place_numbers_image.resize((100, 100), PIL.Image.Resampling.LANCZOS))
        self.Stats_screen = StatsScreen(self.root)
        self.style1 = ttk.Style()
        self.style1.theme_create("notebook_style_catan", settings={
            "TNotebook":
                {"configure":
                     {"background": "DeepSkyBlue4"}},
            "TNotebook.Tab":
                {"configure":
                     {"background": "SkyBlue2",
                      "font": "Arial 15"},
                 "map":
                     {"background": [("selected", "SkyBlue3")],  # when selected
                      "expand": [("selected", [0, 5, 0, 0])]}}  # when selected the expanding of the tab
        })
        self.style1.configure("Catan_game_style.TNotebook", highlightbackground="black", highlightthickness=3)
        self.style1.theme_use("notebook_style_catan")
        self.resources_label = tk.Label(self.root, text="resources: ", bg="#2596be", font="Arial 15")
        self.images_recourses = [ImageTk.PhotoImage(Image.open(fr"assets\bricks.png").convert("RGBA")),
                                 ImageTk.PhotoImage(Image.open(fr"assets\iron.png").convert("RGBA")),
                                 ImageTk.PhotoImage(Image.open(fr"assets\wheat.png").convert("RGBA")),
                                 ImageTk.PhotoImage(Image.open(fr"assets\wood.png").convert("RGBA")),
                                 ImageTk.PhotoImage(Image.open(fr"assets\wool.png").convert("RGBA"))]
        self.count_recourses = [0, 0, 0, 0, 0]
        self.lbl_recourse1 = tk.Label(self.root, image=self.images_recourses[0], bg="#2596be")
        self.lbl_recourse2 = tk.Label(self.root, image=self.images_recourses[1], bg="#2596be")
        self.lbl_recourse3 = tk.Label(self.root, image=self.images_recourses[2], bg="#2596be")
        self.lbl_recourse4 = tk.Label(self.root, image=self.images_recourses[3], bg="#2596be")
        self.lbl_recourse5 = tk.Label(self.root, image=self.images_recourses[4], bg="#2596be")
        self.list_of_labels = [self.lbl_recourse1, self.lbl_recourse2, self.lbl_recourse3, self.lbl_recourse4,
                               self.lbl_recourse5]
        self.count_labels_recourses = tk.Label(self.root,
                                               text=f"{self.count_recourses[0]}        {self.count_recourses[1]}        {self.count_recourses[2]}        {self.count_recourses[3]}        {self.count_recourses[4]}",
                                               font="Arial 15", bg="#2596be")
        self.turn_who_label = tk.Label(self.root, text="", font="Arial 15", bg="#2596be")
        self.dict_colors_indexes = {"bricks": 4, "iron": 3, "wheat": 2, "lumber": 1, "field": 0}
        self.dict_colors_players_indexes = {"firebrick4": 0, "SteelBlue4": 1, "chartreuse4": 2, "#DBB600": 3}





    def start(self):
        try:
            print("meow")
            client_socket = self.connect_to_server(self.ip, self.port)

            self.submit_btn["command"] = lambda: self.check_in(client_socket)
            self.register_btn["command"] = lambda: self.register_menu()
            self.register_account_btn["command"] = lambda: self.register_account(client_socket)
            self.back_btn["command"] = lambda: self.back_to_the_menu(conn=client_socket)
            self.profile_btn["command"] = lambda: self.profile_menu(client_socket)
            self.game_rooms_lobby_btn["command"] = lambda: self.Game_rooms_lobby_menu(client_socket)
            self.root.bind("<Escape>", lambda x: self.back_to_the_menu(conn=client_socket))
            self.refresh_button["command"] = lambda: self.refresh_lobby_rooms(client_socket,
                                                                              client_commands["get_lobby_rooms_cmd"])
            self.create_lobby_game_room_button["command"] = lambda: self.create_lobby_game_room()
            self.create_lobby_game_room_create_button["command"] = lambda: self.send_create_game_room_lobby(
                client_socket)

            # send_connection_thread = threading.Thread(target=self.send_messages, args=(client_socket,))
            # send_connection_thread.start()
            if not self.second_time_connect:
                receive_connection_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
                receive_connection_thread.daemon = True
                receive_connection_thread.start()
                # while True:
                # data = client_socket.recv(1024).decode()

                self.scrollbar["command"] = self.game_rooms_lobby_canvas.yview
                self.game_rooms_lobby_canvas["yscrollcommand"] = self.scrollbar.set
                self.maximum_players_entry.focus_set()

                # packs login
                self.lbl_welcome_message.pack()
                self.name1.pack()
                self.name1_input.pack()
                self.password1.pack()
                self.password1_input.pack()
                self.submit_btn.pack()
                self.lbl1_message.pack()
                self.register_btn.pack()
                self.name1_input.focus()
            else:
                self.current_lobby = "game_rooms_lobby"
                self.main_server = True
                receive_connection_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
                receive_connection_thread.daemon = True
                receive_connection_thread.start()
                self.send_messages(client_socket, client_commands["login_cmd"], "%s#%s" % (self.username, self.password))
                self.Game_rooms_lobby_menu(conn=client_socket)
                self.create_lobby_game_room_create_button["state"] = tk.NORMAL
                time.sleep(2)
                self.second_time_connect = False

            self.root.mainloop()

        except socket.error as e:
            print(e)

    def receive_messages(self, conn):
        try:
            while True:
                data = conn.recv(1024).decode()
                self.handle_received_connection(conn, data)
        except BaseException:
            print(traceback.format_exc())
            return

    def send_messages(self, conn, data, msg=""):
        try:
            while True:
                message = protocol_library.build_message(data, msg)
                print(f"[Client] {message}")
                conn.sendall(message.encode())
                break
        except ConnectionResetError:
            print("hi meow")
            self.back_btn["text"] = "Back"
            self.second_time_connect = True
            self.not_in_waiting_room_lobby_menu()
            self.refresh_lobby_rooms(from_refresh=False)
            self.start()

    def handle_received_connection(self, conn, data):
        print(f"[Server] {data}")
        cmd, msg = protocol_library.disassemble_message(data)
        if self.main_server:
            if cmd == server_commands["login_ok_cmd"]:
                if not self.second_time_connect:
                    self.lbl1_message["text"] = "login succeeded"
                    print("login succeeded")
                    self.login_try_count = 0
                    self.open_menu()
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
                games_played, games_win, self.Email = msg.split("#")
                self.lbl_games_played["text"] = "Games played: " + games_played
                self.lbl_games_wins["text"] = "Win Games: " + games_win
                self.lbl_email["text"] = "E-mail address: " + self.Email
            elif cmd == server_commands["get_lr_ok_cmd"]:
                lobby_rooms = json.loads(msg)
                print(lobby_rooms)
                self.show_game_rooms(lobby_rooms, conn)
            elif cmd == server_commands["create_room_game_lobby_ok_cmd"]:
                conn.close()
                ip1_game_room_lobby_server, port1_game_room_lobby_server, session_id = msg.split("#")
                conn = self.connect_to_game_room_server(ip1_game_room_lobby_server, port1_game_room_lobby_server)
                self.waiting_room_lobby_menu([(self.username, colors[0])], session_id, conn=conn)
                self.send_messages(conn, client_commands["join_my_player_cmd"], self.username)
                self.main_server = False
            elif cmd == server_commands["join_player_game_room_server_ok_cmd"]:
                conn.close()
                msg = msg.split("#")
                self.join_room_game_lobby(msg[0], msg[2], msg[1], msg[3])
            elif cmd == server_commands["join_player_game_room_server_failed_cmd"]:
                self.message_failed_join_error_game["text"] = msg
                self.message_failed_join_error_game.place(x=465, y=115)
                return
        else:
            if cmd == server_game_rooms_commands["join_player_ok_cmd"]:
                print("meow meow hav hav")
                self.update_list_of_players(json.loads(msg))
            elif cmd == server_game_rooms_commands["close_lobby_ok_cmd"]:
                print(msg)
                conn.close()
                self.back_to_the_menu()
            elif cmd == server_game_rooms_commands["get_players_information_ok"]:
                self.update_list_of_players(msg)
            elif cmd == server_game_rooms_commands["leave_player_ok_cmd"]:
                self.update_list_of_players(json.loads(msg))
            elif cmd == server_game_rooms_commands["buy_building_ok_cmd"]:
                self.handle_buttons(msg)
            elif cmd == server_game_rooms_commands["start_game_ok"]:
                self.tiles = self.tiles + json.loads(msg, object_hook=lambda d: SimpleNamespace(**d))  # , self.ports , self.ports + json.loads(temp1)
                print(len(self.tiles))
                if self.bytes_times_counter == 8:
                    self.bytes_times_counter = 0
                    self.start_game(conn)
                else:
                    self.bytes_times_counter += 1
            elif cmd == server_game_rooms_commands["pulled_cubes_cmd"]:
                msg = msg.split("#")
                results = json.loads(msg[0])
                recourses = json.loads(msg[1])
                self.count_recourses = recourses
                self.pull_cubes(results)
            elif cmd == server_game_rooms_commands["turn_who_cmd"]:
                msg = msg.split("#")
                self.turn_who_label["text"] = "The turn of " + dict_colors[msg[0]]
                self.turn_who_label["foreground"] = msg[0]
                if msg[1] == self.username:
                    self.button_buy_settlement["state"] = tk.NORMAL

    def check_in(self, conn):
        self.username, self.password = (self.name1_input.get(), self.password1_input.get())
        print(self.password)
        if self.username == "":
            self.lbl1_message["text"] = "the username isn't empty"
            print("the username isn't empty")
        elif self.password == "":
            self.lbl1_message["text"] = "the password isn't empty"
            print("the password isn't empty")
        elif not protocol_library.check_username_validability(self.username):
            self.lbl1_message["text"] = "the syntax of the username is not valid"
            print("the syntax of the username is not valid")
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
        elif not protocol_library.check_username_validability(self.username):
            self.lbl2_message["text"] = "the username must be built from characters between a-z, A-Z, 0-9 (including)"
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
            self.current_lobby = "login"
        # packs login
        self.lbl_welcome_message.pack()
        self.name1.pack()
        self.name1_input.pack()
        self.password1.pack()
        self.password1_input.pack()
        self.submit_btn.pack()
        self.lbl1_message.pack()
        self.register_btn.pack()
        self.name1_input.focus_force()

    def back_to_the_menu(self, event=None, conn=None):
        if self.current_lobby == "register":
            self.not_in_register_menu()
            self.login_menu()
        elif self.current_lobby == "main_lobby":
            self.not_in_main_lobby()
            self.send_messages(conn, client_commands["logout_cmd"])
            self.login_menu()
        elif self.current_lobby == "profile":
            self.not_in_profile_menu()
            self.open_menu()
        elif self.current_lobby == "game_rooms_lobby":
            self.refresh_lobby_rooms(from_refresh=False)
            self.not_in_Game_rooms_lobby_menu()
            self.open_menu()
        elif self.current_lobby == "creating_game_lobby_room":
            self.refresh_lobby_rooms(from_refresh=False)
            self.not_in_create_lobby_game_room()
            self.Game_rooms_lobby_menu(conn)
        elif self.current_lobby == "waiting_game_room_lobby":
            time.sleep(2)
            self.back_btn["text"] = "Back"
            self.second_time_connect = True
            self.not_in_waiting_room_lobby_menu()
            self.start()
            self.refresh_lobby_rooms(from_refresh=True)

    def not_in_main_lobby(self):
        self.lbl1_welcome_message.pack_forget()
        if self.current_lobby != "profile" and self.current_lobby != "game_rooms_lobby":
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
        self.lbl_email["text"] = self.Email
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

    def Game_rooms_lobby_menu(self, conn):
        self.current_lobby = "game_rooms_lobby"
        self.not_in_main_lobby()
        self.game_rooms_lobby_lbl.place(x=483, y=50)
        self.scrollbar_frame.pack(fill=tk.BOTH, padx=300, pady=150)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.games_rooms_list.pack()
        self.game_rooms_lobby_canvas.pack()
        self.refresh_button.place(x=300, y=650)
        self.create_lobby_game_room_button.place(x=974, y=650)
        if not self.from_creating and not self.from_main_lobby and not self.from_lobby_game_waiting_or_in_actual_game:
            self.send_messages(conn, client_commands["get_lobby_rooms_cmd"])

    def not_in_Game_rooms_lobby_menu(self):
        self.game_rooms_lobby_lbl.place_forget()
        self.scrollbar_frame.pack_forget()
        self.scrollbar.pack_forget()
        # self.games_rooms_list.pack_forget()
        self.game_rooms_lobby_canvas.pack_forget()
        self.create_lobby_game_room_button.place_forget()
        self.refresh_button.place_forget()
        self.message_failed_join_error_game.place_forget()

    def on_mousewheel(self, event):
        self.game_rooms_lobby_canvas.yview_scroll(-1*event.delta//120, "units")  # the speed of scrolling and the units of it?

    def show_game_rooms(self, game_rooms_dict, conn):
        """self.scrollbar_frame.pack_forget()
        self.scrollbar.pack_forget()
        self.scrollbar_frame.pack(fill=tk.BOTH, padx=300, pady=150)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.game_rooms_lobby_canvas.pack_forget()
        self.game_rooms_lobby_canvas.pack()"""
        if game_rooms_dict == {}:
            self.game_rooms_lobby_canvas.delete("all")
            self.game_rooms_lobby_canvas.create_text(675, 195, text="There are no game lobby rooms", font="Arial 16", anchor=tk.CENTER, state=tk.DISABLED)
        else:
            space = 0
            for lobby_room1 in game_rooms_dict:
                # lbl1 = tk.Label(self.game_rooms_lobby_canvas, text=game_rooms_dict[lobby_room1][0], font="Arial 11")
                # lbl1.place(x=100, y=100)
                creator, max_players, is_full, players, port_server = game_rooms_dict[lobby_room1]
                print(game_rooms_dict[lobby_room1])
                rectangle1 = self.game_rooms_lobby_canvas.create_rectangle(353, 170 + space, 985, 300 + space, activewidth=3, width=2, fill="#AFABAB")
                self.game_rooms_lobby_canvas.create_text(370, 195 + space, text=f"{creator}'s looby room", font="Arial 16", fill="black", state=tk.DISABLED, anchor=tk.NW)
                self.game_rooms_lobby_canvas.create_text(370, 230 + space, text=f"Number of players: {players} out of {max_players}", font="Arial 14", fill="black", state=tk.DISABLED, anchor=tk.NW)
                space += 170
                position1 = int(self.game_rooms_lobby_canvas["height"])
                self.game_rooms_lobby_canvas["height"] = position1 + space
                self.game_rooms_lobby_canvas.configure(scrollregion=(300, 150, 900, 150 + space))
                button_join_game = tk.Button(self.scrollbar_frame, text="Join", relief="solid", bg="#70ad47", font="Arial 15", command=lambda: self.send_messages(conn, client_commands["join_game_room_cmd"], lobby_room1))
                if is_full:
                    button_join_game["state"] = tk.DISABLED
                button_join_game.place(x=500, y=170 + space)
                canvas_window = self.game_rooms_lobby_canvas.create_window(950, 100 + space, window=button_join_game)
                self.game_rooms_lobby_canvas.itemconfigure(rectangle1, state=tk.NORMAL)

    def create_lobby_game_room(self):
        self.current_lobby = "creating_game_lobby_room"
        self.not_in_Game_rooms_lobby_menu()
        self.lobby_name_game_room_lbl["text"] = f"Waiting room - {self.username}'s lobby"
        self.lobby_name_game_room_lbl.pack(padx=450, pady=20, side=tk.TOP)
        self.game_room_lobby_create_canvas.place(x=350, y=100)
        self.maximum_players_lbl.place(x=360, y=180)
        self.maximum_players_entry.place(x=702, y=180)
        self.create_lobby_game_room_create_button.place(x=890, y=330)

    def refresh_lobby_rooms(self, conn="", cmd="", msg="", from_refresh=True):
        # self.not_in_Game_rooms_lobby_menu()
        if from_refresh:
            self.message_failed_join_error_game.place_forget()  # even if the label is not placed it won't do an error
            self.game_rooms_lobby_canvas.delete("all")
            self.send_messages(conn, cmd, msg)
        self.refresh_button["state"] = tk.DISABLED
        self.from_creating = True
        self.from_main_lobby = True
        self.from_lobby_game_waiting_or_in_actual_game = True
        if not self.is_active:
            self.root.after(5000, lambda: self.set_refresh_button_enabled())  # self.refresh_button disabled for 5 seconds
            self.is_active = True

    def not_in_create_lobby_game_room(self):
        if self.current_lobby != "waiting_game_room_lobby":
            self.lobby_name_game_room_lbl.pack_forget()
        self.game_room_lobby_create_canvas.place_forget()
        self.maximum_players_entry.place_forget()
        self.maximum_players_lbl.place_forget()
        self.create_lobby_game_room_create_button.place_forget()
        self.number_players_not_valid.place_forget()

    def send_create_game_room_lobby(self, conn):
        maximum_players1 = self.maximum_players_entry.get()
        print(maximum_players1)
        if maximum_players1 in ("2", "3", "4"):
            self.send_messages(conn, client_commands["create_game_room_lobby_cmd"], maximum_players1)
            self.create_lobby_game_room_create_button["state"] = tk.DISABLED
        else:
            self.number_players_not_valid.place(x=360, y=260)

    def set_refresh_button_enabled(self):
        self.refresh_button["state"] = tk.NORMAL
        self.from_creating = False
        self.from_main_lobby = False
        self.is_active = False
        self.from_lobby_game_waiting_or_in_actual_game = False

    def waiting_room_lobby_menu(self, list_of_names: list, session_id="", from_creating=True, conn = None):
        self.current_lobby = "waiting_game_room_lobby"
        if from_creating and conn is not None:
            self.not_in_create_lobby_game_room()
            self.back_btn["text"] = "Close lobby"
            self.start_game_menu_button.place(x=1070, y=500)
            self.start_game_menu_button["command"] = lambda: self.send_messages(conn, client_commands["start_game_cmd"])
        else:
            self.not_in_Game_rooms_lobby_menu()
            self.back_btn["text"] = "Leave Room"
            self.name_leader["text"] = f"Waiting room - {list_of_names[0][0]}'s lobby"
            self.back_btn["command"] = lambda: self.leave_room_game_lobby(conn)
            print("button is set")
            self.name_leader.pack(padx=450, pady=20, side=tk.TOP)
        self.waiting_room_lobby_menu_canvas.place(x=240, y=150)
        self.waiting_to_start_lbl["text"] = f"Waiting for {list_of_names[0][0]} to start the game"
        self.session_id_lbl["text"] = "Game room id: " + session_id
        self.waiting_to_start_lbl.pack(padx=400, pady=10, side=tk.TOP)
        self.session_id_lbl.place(x=920, y=180)
        self.participants_lbl["text"] = "Players:"
        space = 0
        self.participants_lbl.place(x=280, y=180)
        print(list_of_names)
        for name, color in list_of_names:
            print("meow hav 1 1")
            self.waiting_room_lobby_menu_canvas.create_text(50, 70 + space, text=name, fill=color, font="Arial 17", state=tk.DISABLED, anchor=tk.NW)
            space += 30

    def connect_to_game_room_server(self, ip2, port2, leader_lobby_game_room=True):
        try:
            self.ip2 = ip2
            self.port2 = int(port2)
            print(ip2, port2)
            conn = self.connect_to_server(self.ip2, self.port2)
            receive_connection_thread = threading.Thread(target=self.receive_messages, args=(conn,))
            receive_connection_thread.daemon = True
            receive_connection_thread.start()
            if leader_lobby_game_room:
                self.back_btn["command"] = lambda: self.send_messages(conn, client_commands["close_lobby_cmd"])
            else:
                self.back_btn["command"] = lambda: self.leave_room_game_lobby(conn)
            print(f"you have been switched to game room lobby menu server: ip :{self.ip2}, port :{self.port2}")
            return conn
        except socket.error as e:
            print(e)
            print("meow hav meow hav 1 2 1 2", conn)

    def connect_to_server(self, ip_server, port_server):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_server, port_server))
        print(client_socket)
        return client_socket

    def not_in_waiting_room_lobby_menu(self):
        self.lobby_name_game_room_lbl.pack_forget()
        self.start_game_menu_button.place_forget()
        self.waiting_room_lobby_menu_canvas.delete()
        self.waiting_room_lobby_menu_canvas.place_forget()
        self.waiting_to_start_lbl.pack_forget()
        self.session_id_lbl.place_forget()
        self.participants_lbl.place_forget()
        self.name_leader.pack_forget()

    def update_list_of_players(self, new_list_of_players):
        if self.current_lobby == "waiting_game_room_lobby":
            space = 0
            self.waiting_room_lobby_menu_canvas.delete("all")
            for name, color in new_list_of_players:
                self.waiting_room_lobby_menu_canvas.create_text(50, 70 + space, text=name, fill=color,
                                                                font="Arial 17", state=tk.DISABLED, anchor=tk.NW)
                space += 30
            self.list_of_players = new_list_of_players

    def join_room_game_lobby(self, ip1, port1, session_id, leader_name):
        conn1 = self.connect_to_game_room_server(ip1, port1)
        self.main_server = False
        self.send_messages(conn1, client_commands["join_my_player_cmd"], self.username)
        self.waiting_room_lobby_menu([leader_name, colors[0]], session_id, False, conn1)

    def leave_room_game_lobby(self, conn):
        print("meow meow hav bye hav")
        self.send_messages(conn, client_commands["leave_my_player_cmd"])
        time.sleep(2)
        conn.close()
        self.back_to_the_menu()

    def start_game(self, conn):
        self.not_in_waiting_room_lobby_menu()
        self.configure_tiles()
        self.canvas_game.pack(side=tk.LEFT)
        self.canvas_game["height"] = self.root.winfo_screenheight()
        self.draw_map()
        self.Stats_screen.start(sorted(self.list_of_players, key=lambda x: x[0]))  # only the players from (players, colors) and start a Stats_screen
        for index, placement1 in enumerate(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1]):
            id_placement = self.canvas_game.create_image(placement1[0], placement1[1], image=self.none_any_circle,
                                                    activeimage=self.Circle_choosing_photo_image, tags="circle_tag")
            print(id_placement, end=", ")
            self.ids_placements.append(id_placement)
            i = self.canvas_game.create_text(placement1[0], placement1[1], text=str(index), state=tk.DISABLED,
                                        tags="indexes_texts_rectangles")
            r = self.canvas_game.create_rectangle(self.canvas_game.bbox(i), fill="#2596be", tags="indexes_texts_rectangles")
            self.canvas_game.itemconfigure(i, state=tk.HIDDEN)
            self.canvas_game.itemconfigure(r, state=tk.HIDDEN)
            self.canvas_game.tag_lower(r, i)
            # self.canvas.tag_bind(id_placement, "<Button-1>", lambda x: self.canvas.itemconfigure(self.canvas.find_withtag(), image=self.Circle_choosing_photo_image))
        self.button_buy_road.place(x=self.root.winfo_screenwidth() - 125, y=self.root.winfo_screenheight() - 420)
        self.button_buy_boat.place(x=self.root.winfo_screenwidth() - 250, y=self.root.winfo_screenheight() - 420)
        self.button_buy_settlement.place(x=self.root.winfo_screenwidth() - 430, y=self.root.winfo_screenheight() - 420)
        self.button_buy_city.place(x=self.root.winfo_screenwidth() - 112, y=self.root.winfo_screenheight() - 360)
        self.button_buy_development_card.place(x=self.root.winfo_screenwidth() - 352,
                                               y=self.root.winfo_screenheight() - 360)
        self.button_declare_victory.place(x=self.root.winfo_screenwidth() - 174, y=self.root.winfo_screenheight() - 300)
        self.button_next_turn.place(x=self.root.winfo_screenwidth() - 367, y=self.root.winfo_screenheight() - 300)
        self.button_buy["command"] = lambda: self.close_placements(conn)
        # self.canvas.tag_lower("road", "settlement")
        # self.canvas.tag_lower("road", "city")
        self.button_pull_cubes["command"] = lambda: self.send_messages(conn=conn,
                                                                       data=client_commands["pull_cubes_cmd"], msg="")
        self.button_pull_cubes.place(x=self.root.winfo_screenwidth() - 450, y=self.root.winfo_screenheight() - 150)
        self.button_pull_cubes.place(x=self.root.winfo_screenwidth() - 450, y=self.root.winfo_screenheight() - 150)
        self.resources_label.place(x=self.root.winfo_screenwidth() - 450, y=self.root.winfo_screenheight() - 100)
        for i in range(5):
            self.list_of_labels[i].place(x=self.root.winfo_screenwidth() - 60 * i - 50, y=self.root.winfo_screenheight() - 100)
            self.count_labels_recourses.place(x=self.root.winfo_screenwidth() - 57 * i - 50,
                                              y=self.root.winfo_screenheight() - 50)
        self.turn_who_label.place(x=self.root.winfo_screenwidth() - 350, y=10)

    def draw_map(self):
        for index, tile_image in enumerate(self.tiles_images):
            if self.tiles[index].terrain_kind != "sea":
                self.canvas_game.create_image(self.tiles[index].placement[0], self.tiles[index].placement[1], image=tile_image[0])
                self.canvas_game.create_image(self.tiles[index].placement[0], self.tiles[index].placement[1], image=self.place_numbers_image)
                self.canvas_game.create_image(self.tiles[index].placement[0], self.tiles[index].placement[1], image=tile_image[1])
            else:
                self.canvas_game.create_image(self.tiles[index].placement[0], self.tiles[index].placement[1], image=tile_image)
            # self.canvas_game.create_text(self.tiles[index].placement[0], self.tiles[index].placement[1], text=self.index)
        # for index in range(len(self.tiles)):
        # for index1, middle in enumerate(placements_middle_hexes_vertex_hexes[index][0]):
        #     self.canvas.create_text(middle[0], middle[1], text=str(index1))
        # for index1, vertex in enumerate(placements_middle_hexes_vertex_hexes[index][1]):
        #     self.canvas.create_text(vertex[0], vertex[1], text=str(index1))
        # for index1, placement1 in enumerate(placements_parts_builds_in_game[0]):
        #     self.canvas.create_text(placement1[0], placement1[1], text=str(index1))
        # for index1, placement1 in enumerate(placements_parts_builds_in_game[0]):
        #     self.canvas.create_text(placement1[0], placement1[1], text=str(index1))
        # for index1, port in enumerate(self.ports):
        #     port.draw_port(self.canvas)

    def close_placements(self, conn):
        self.place_entry.place_forget()
        self.button_buy.place_forget()
        self.cancel_buying_button.place_forget()
        self.where_place.place_forget()
        for item in self.canvas_game.find_withtag("indexes_texts_rectangles"):
            print(item, end=", ")  # not to delete
            self.canvas_game.itemconfigure(item, state=tk.HIDDEN)
        position1 = self.place_entry.get()
        if position1 != "":
            for element in position1:
                if element not in "1234567890":
                    return "an index is in numbers"
        position1 = int(position1)
        if (0 <= position1 <= 154 and (self.current_button == "road" or self.current_button == "boat")) or (267 > position1 > 154 and (self.current_button == "city" or self.current_button == "settlement")):
            self.send_messages(conn, client_commands["buy_building_cmd"], f"{position1}#{self.current_button}")
        else:
            return "there was an error, check again your input"

    def handle_buttons(self, msg):
        building = json.loads(msg, object_hook=lambda d: SimpleNamespace(**d))
        print(building.type1)
        if building.type1 == "Road":
            building = Road(building.color, building.index, building.position)
            self.roads.append((building.index, building))
            building.draw_road(self.canvas_game)
            self.canvas_game.tag_lower("road",
                                  "settlement")  # that for the assuming that roads are built after placing settlements and over and more
            for tile in what_part_is_on_what_tile_hex[0][building.index]:
                if tile is not None:
                    tile = self.tiles[tile]
                    tile.add_building(building, places_in_each_placements_for_the_hexes[0][building.index],
                                      is_settlement_or_city=False)
                    print(tile)
        elif building.type1 == "Boat":
            building = Boat(building.color, building.index, building.position, self.image_boat_1)
            building.image = self.image_boat_1
            self.boats.append((building.index, building))
            for tile in what_part_is_on_what_tile_hex[0][building.index]:
                if tile is not None:
                    tile = self.tiles[tile]
                    tile.add_building(building, places_in_each_placements_for_the_hexes[0][building.index],
                                      is_settlement_or_city=False)
                    print(tile)
            building.draw_boat(self.canvas_game)
            self.canvas_game.tag_lower("boat",
                                  "settlement")  # that for the assuming that roads are built after placing settlements and over and more
            # and in order to see the boat's image
            self.canvas_game.tag_lower("road", "boat")
        elif building.type1 == "City":
            for index, settlement in self.settlements:
                if index == building.index and settlement.color == "red":
                    building.img = self.image_city_red
                    building = City(building.color, building.index, building.position, building.img)
                    self.canvas_game.delete(settlement.id)
                    self.settlements.remove((index, settlement))
                    building.draw_city(self.canvas_game)
                    self.cities.append((building.index, building))
                    for index2, tile_index in enumerate(
                            [index for index in what_part_is_on_what_tile_hex[1][building.index - 155]]):
                        if tile_index is not None:
                            tile_index1 = self.tiles[tile_index]
                            tile_index1.delete_building(
                                places_in_each_placements_for_the_hexes[1][building.index - 155][index2])
                            tile_index1.add_building(building, places_in_each_placements_for_the_hexes[1][building.index - 155][
                                index2], is_settlement_or_city=False)
                            print(index2, tile_index1, tile_index)
                    print(self.settlements)
                    print(self.cities)
                    break
        elif building.type1 == "Settlement":
            building.img = self.image1
            building = Settlement(building.color, building.index, building.position, building.img)
            building.draw_settlement(self.canvas_game)
            index2 = 0
            for index1 in [index for index in what_part_is_on_what_tile_hex[1][building.index - 155]]:
                if index1 is not None:
                    tile = self.tiles[index1]
                    print(tile, index1)
                    tile.add_building(building=building,
                                      index1=places_in_each_placements_for_the_hexes[1][building.index - 155][index2],
                                      is_settlement_or_city=True)
                index2 += 1
            self.settlements.append((building.index, building))
            self.button_buy_boat["state"] = tk.NORMAL
            self.button_buy_road["state"] = tk.NORMAL

    def change_current_button(self, new_current):
        self.current_button = new_current
        self.place_entry.place(x=self.root.winfo_screenwidth() - 300, y=self.root.winfo_screenheight() - 200)
        self.button_buy.place(x=self.root.winfo_screenwidth() - 125, y=self.root.winfo_screenheight() - 150)
        self.where_place["text"] = f"Where to place your {self.current_button}?"
        self.where_place.place(x=self.root.winfo_screenwidth() - 300, y=self.root.winfo_screenheight() - 230)
        self.cancel_buying_button.place(x=self.root.winfo_screenwidth() - 300,
                                        y=self.root.winfo_screenheight() - 150)
        for item in self.canvas_game.find_withtag("indexes_texts_rectangles"):
            print(item, end=", ")  # not to delete
            self.canvas_game.itemconfigure(item, state=tk.DISABLED)

    def pull_cubes(self, results):
        self.button_buy_city["state"] = tk.NORMAL
        self.button_buy_boat["state"] = tk.NORMAL
        self.button_buy_road["state"] = tk.NORMAL
        self.button_next_turn["state"] = tk.NORMAL
        self.button_buy_settlement["state"] = tk.NORMAL
        self.button_buy_development_card["state"] = tk.NORMAL
        self.button_declare_victory["state"] = tk.NORMAL
        self.lbl_cube1["image"] = self.cubes_images[results[0] - 1]
        self.lbl_cube2["image"] = self.cubes_images[results[1] - 1]
        self.lbl_cube1.place(x=self.root.winfo_screenwidth() - 450, y=self.root.winfo_screenheight() - 210)
        self.lbl_cube2.place(x=self.root.winfo_screenwidth() - 390, y=self.root.winfo_screenheight() - 210)
        self.sum_cubes_lbl["text"] = str(results[2])
        self.sum_cubes_lbl.place(x=self.root.winfo_screenwidth() - 340, y=self.root.winfo_screenheight() - 135)
        print(self.count_labels_recourses)
        self.count_labels_recourses["text"] = f"{self.count_recourses[0]}        {self.count_recourses[1]}        {self.count_recourses[2]}        {self.count_recourses[3]}        {self.count_recourses[4]}"

    def configure_tiles(self):
        for tile in self.tiles:
            self.tiles[tile.index] = TerrainTile1(tile.number, tile.placement, tile.terrain_kind, tile.index)
        for tile in self.tiles:
            image1 = ImageTk.PhotoImage(Image.open(fr"assets\{tile.terrain_kind}_hex_rotated1.png").convert("RGBA").resize((150, int(150 * (258 / 269))),
                                                                      PIL.Image.Resampling.LANCZOS))  # resampling is the change from the PIL module update
            if tile.terrain_kind != "sea":
                image_number = self.numbers1_image.crop((0 + 40 * (tile.number - 1) - 2, 0, 0 + 40 * tile.number, 40))
                image_number = ImageTk.PhotoImage(image_number.resize((30, 30), PIL.Image.Resampling.LANCZOS))
                self.tiles_images.append((image1, image_number))
            else:
                self.tiles_images.append(image1)

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 23478
    client1 = Client(ip, port)
    client1.start()
