
client_commands = {
    "login_cmd": "LOGIN",
    "logout_cmd": "LOGOUT",
    "sign_up_cmd": "SIGN_UP",
    "get_profile_cmd": "GET_PROFILE",
    "get_lobby_rooms_cmd": "GET_LOBBY_ROOMS",
    "join_my_player_cmd": "JOIN_PLAYER",
    "get_players_information_cmd": "GET_PL_IN",
    "start_game_cmd": "START_GAME",
    "create_game_room_lobby_cmd": "CREATE_ROOM"
}

server_commands = {
    "login_ok_cmd": "LOGIN_OK",
    "login_failed_cmd": "LOGIN_FAILED",
    "sign_up_ok_cmd": "SIGN_UP_OK",
    "sign_up_failed": "SIGN_UP_FAILED",
    "get_profile_ok": "GET_PROFILE_OK",
    "get_lr_ok_cmd": "GET_LR_OK",
    "create_room_game_lobby_ok_cmd": "CREATE_ROOM_OK"
}

server_game_rooms_commands = {
    "join_player_ok_cmd": "JOIN_PLAYER_OK",
    "join_player_failed_cmd": "JOIN_PL_FAILED",
    "get_players_information_ok": "GET_PL_IN_OK",
    "start_game_ok": "START_GAME_OK"
}

def build_message(cmd, msg=""):
    """
    builds a message of the protocol with the parameters.
    :param cmd: command
    :param msg: message
    :rtype: string
    :return: A message of the protocol
    """
    message = cmd + " " * (16 - len(cmd)) + "|" + str(len(msg)).zfill(4) + "|" + msg
    return message


def disassemble_message(message):
    """
    disassembles an already built message
    :param message: A message of the protocol
    :return: cmd (string), msg (string)
    """
    cmd = message[:16].replace(" ", "")  # the command without spaces and whitespaces
    msg = message[22:]  # the msg, could be empty
    return cmd, msg
