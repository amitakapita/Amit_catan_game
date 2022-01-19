import tkinter as tk

root = tk.Tk()  # Tk and not TK
root.title("Catan Game")
root.geometry("500x500+30+30")

# Constants:
accounts = {"meow": "meow", "test": "1234"}

count1 = 1


def check_in():
    global count1
    username, password = name1_input.get(), password1_input.get()
    if count1 != 3:
        count1 += 1
        if username in accounts.keys():
            if password in accounts.values():
                lbl1_message["text"] = "login succeeded"
                count1 = 1
            else:
                lbl1_message["text"] = "the password is incorrect"
        elif username == "":
            lbl1_message["text"] = "the username is not empty."
            count1 = 1
        else:
            lbl1_message["text"] = "the username does not exist in the system"
    else:
        if username in accounts.keys() and password in accounts.values():
            lbl1_message["text"] = "login succeeded"
            count1 = 1
        else:
            lbl1_message["text"] = "login locked"
            submit_btn["state"] = tk.DISABLED
            name1_input["state"] = tk.DISABLED
            password1_input["state"] = tk.DISABLED
    # lbl1_message.pack()


# Labels and Entryies
name1 = tk.Label(root, text="Username: ")
name1_input = tk.Entry(root, font="Arial 13")
password1 = tk.Label(root, text="Password: ")
password1_input = tk.Entry(root, font="Arial 13", show="*")
submit_btn = tk.Button(root, text="Login", relief="solid", command=check_in)
lbl1_message = tk.Label(root)


# packs
name1.pack()
name1_input.pack()
password1.pack()
password1_input.pack()
submit_btn.pack()
lbl1_message.pack()

root.mainloop()
