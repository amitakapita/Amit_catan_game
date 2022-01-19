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
