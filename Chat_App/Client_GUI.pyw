from tkinter import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

is_name = True


def recv_message(root, sock, chat_box):
    while True:
        try:
            msg = sock.recv(1024).decode()
            chat_box.insert(END, msg)
        except ConnectionAbortedError:
            """ if GUI closes"""
            break
        except ConnectionResetError:
            """ if server closes the connection"""
            sock.close()
            chat_box.insert(END, "Server has closed the connection.Closing...")
            sleep(3)
            root.quit()
            break


def send_message(sock, entry_var, chat_box):
    """ when user sending his name should not shown in the chat """
    try:
        global is_name
        msg = entry_var.get()
        sock.send(msg.encode())
        entry_var.set("")
        if not is_name:
            chat_box.insert(END, msg)
        is_name = False
    except ConnectionAbortedError:
        """
        when server closed the connection and while recv_message function waits for 3
        second if user tries to send something this error could occur and we ignore it
        """
        pass


def on_closing(sock, root):
    sock.close()
    root.quit()


def create_socket(host, port):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        start_GUI(sock)
    except ConnectionRefusedError:
        print("Connection Refused!(Server might be closed)")  # GUI does not initialize
        sleep(3)


def start_GUI(sock):
    # ---------------------------------------------creates the GUI------------------------------------------------------
    root = Tk()
    root.title("Chat App")
    root.geometry("450x500+350+200")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(sock, root))
    # root.configure(background="")

    entry_var = StringVar()
    frame = Frame(root)
    chat_box = Listbox(frame, height=20, borderwidth=1, relief="solid")
    msg_box = Entry(root, width=50, textvariable=entry_var, borderwidth=1, relief="solid")
    msg_box.bind("<Return>", lambda event: send_message(sock, entry_var, chat_box))
    scrollbar = Scrollbar(frame, command=chat_box.yview, orient=VERTICAL)
    chat_box.configure(yscrollcommand=scrollbar.set)

    frame.pack(fill=X, padx=30)
    scrollbar.pack(side=RIGHT, fill=Y, pady=30)
    chat_box.pack(fill=X, pady=30)
    msg_box.pack(fill=X, padx=100, ipady=5)
    # ------------------------------------------------------------------------------------------------------------------
    chat_box.insert(END, "Welcome to the chat room.First type your name and send it.")
    chat_box.insert(END, "Then you are free to chat.")
    chat_box.insert(END, "\n")

    Thread(target=recv_message, args=(root, sock, chat_box)).start()  # starts the thread (infinite loop)

    root.mainloop()  # starts the GUI (infinite loop) // main thread


if __name__ == "__main__":
    host, port = "192.168.1.30", 8000
    create_socket(host, port)   # After creating socket it starts the GUI
