
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from datetime import datetime
import emoji
import sqlite3
from PIL import ImageTk,Image
import os

BUFSIZ=1024
def receive():
    messagesql=[]
    i=0
    global msg
    try:
        mycon=sqlite3.connect('chat_history1010.db')
        st="create table '{0}'(message varchar(1024));".format(IP)
        cursor=mycon.cursor()
        cursor.execute(st)
        mycon.commit()
    except sqlite3.OperationalError:#if table is already created
        pass
    """Handles receiving of messages."""
    while True:
        try:
            msg=client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.insert(tkinter.END, emoji.emojize(msg))
            d=datetime.now()
            m='['+str(d)+']:->'+msg
            messagesql.append(m)

            mycon=sqlite3.connect('chat_history1010.db')
            cursor=mycon.cursor()
            ins="insert into '{0}' values('{1}')".format(IP,m)
            cursor.execute(ins)
            mycon.commit()
            msg_list.itemconfig(i, foreground="fuchsia")
            i=i+1
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    global msg
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

#--="chat history part"=--
def createChatHistory():
    mycon=sqlite3.connect('chat_history1010.db')
    cursor=mycon.cursor()
    cursor.execute("select message from '{0}'".format(IP))
    history=cursor.fetchall()
    newWindow = tkinter.Toplevel()
    for row in history:
        
        l1 = tkinter.Label(newWindow, text = row ,bg="#FFA500")
        l1.pack(side='top', anchor='nw')
    print(row)
def register():
    global register_screen
    register_screen = tkinter.Toplevel(main_screen)
    register_screen.configure(bg="#FFA500")
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global ServerIP
    global ServerPORT
    global IP_entry
    global PORT_entry
    ServerIP = tkinter.StringVar()
    ServerPORT = tkinter.StringVar()

    tkinter.Label(register_screen, text="Please enter details below", bg="cyan").pack()
    tkinter.Label(register_screen, text="",bg="#FFA500").pack()
    IP_lable = tkinter.Label(register_screen, text="IP * ",bg="lime")
    IP_lable.pack()
    IP_entry = tkinter.Entry(register_screen, textvariable=ServerIP,show="*")
    IP_entry.pack()
    PORT_lable = tkinter.Label(register_screen, text="PORT* ",bg="lime")
    PORT_lable.pack()
    PORT_entry = tkinter.Entry(register_screen, textvariable=ServerPORT, )
    PORT_entry.pack()
    tkinter.Label(register_screen, text="",bg="#FFA500").pack()
    tkinter.Button(register_screen, text="Register", width=10, height=1, bg="cyan", command = register_server).pack()

def login():
    global login_screen
    login_screen = tkinter.Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.configure(bg="#FFA500")
    login_screen.geometry("300x250")
    tkinter.Label(login_screen, text="Please enter details below to login",bg="cyan").pack()
    tkinter.Label(login_screen, text="",bg="#FFA500").pack()

    global Server_verify
    global PORT_verify

    Server_verify = tkinter.StringVar()
    PORT_verify = tkinter.StringVar()

    global server_login_entry
    global PORT_login_entry

    tkinter.Label(login_screen, text="IP * ",bg="lime").pack()
    server_login_entry = tkinter.Entry(login_screen, textvariable=Server_verify, show="*")
    server_login_entry.pack()
    tkinter.Label(login_screen, text="",bg="#FFA500").pack()
    tkinter.Label(login_screen, text="Port * ",bg="lime").pack()
    PORT_login_entry = tkinter.Entry(login_screen, textvariable=PORT_verify,)
    PORT_login_entry.pack()
    tkinter.Label(login_screen, text="",bg="#FFA500").pack()
    LOGIN=tkinter.Button(login_screen, text="Login", width=10, height=1, command = login_verify,background="cyan")
    LOGIN["border"]="10"
    LOGIN.pack()

def register_server():
    global IP_info

    IP_info = ServerIP.get()
    PORT_info = ServerPORT.get()

    file = open(IP_info, "w")
    file.write(IP_info + "\n")
    file.write(PORT_info)
    file.close()

    IP_entry.delete(0, tkinter.END)
    PORT_entry.delete(0, tkinter.END)

    tkinter.Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()



def login_verify():
#get IP
    global IP
    global PORT
    IP = Server_verify.get()
    PORT = PORT_verify.get()
# this will delete the entry after login button is pressed
    server_login_entry.delete(0, tkinter.END)
    PORT_login_entry.delete(0, tkinter.END)
  

#defining verification's conditions 
    list_of_files = os.listdir()
    if IP in list_of_files:
        file1 = open(IP, "r")
        verify = file1.read().splitlines()
        if PORT in verify:
            login_sucess()

        else:
            PORT_not_recognised()

    else:
        server_not_found()
def login_sucess():
    global login_success_screen 
    login_success_screen = tkinter.Toplevel(login_screen)
    login_success_screen.configure(bg="lime")
    login_success_screen.title("Success")
    tkinter.Label(login_success_screen, text="Server is Found",justify='center',fg="Green").pack()
    tkinter.Button(login_success_screen, text="OK", command=delete_login_success,bg="cyan").pack()

# Designing popup for login invalid password

def PORT_not_recognised():
    global PORT_not_recog_screen
    PORT_not_recog_screen = tkinter.Toplevel(login_screen)
    PORT_not_recog_screen.configure(bg="Red")
    PORT_not_recog_screen.title("Success")
    PORT_not_recog_screen.geometry("150x100")
    tkinter.Label(PORT_not_recog_screen, text="Invalid PORT",fg="Red").pack()
    tkinter.Button(PORT_not_recog_screen, text="OK", command=delete_PORT_not_recognised).pack()

# Designing popup for user not found
 
def server_not_found():
    global server_not_found_screen
    server_not_found_screen = tkinter.Toplevel(login_screen)
    server_not_found_screen.configure(bg="Red")
    server_not_found_screen.title("Success")
    server_not_found_screen.geometry("150x100")
    tkinter.Label(server_not_found_screen, text="Server Not Found",fg="Red").pack()
    okbutton=tkinter.Button(server_not_found_screen, text="OK", command=delete_server_not_found_screen)
    okbutton["border"]="0"
    okbutton.pack()
# Deleting popups

def delete_login_success():
    login_success_screen.destroy()
    main_screen.destroy()



def delete_PORT_not_recognised():
    PORT_not_recog_screen.destroy()


def delete_server_not_found_screen():
    server_not_found_screen.destroy()
def main_account_screen():
    global main_screen
    main_screen = tkinter.Tk()
    main_screen.configure(bg="#FFA500")
    main_screen.geometry("400x400")
    main_screen.title("Server Login")
    tkinter.Label(text="",bg="#FFA500").pack()
    tkinter.Button(text="Login", height="2", width="30", command = login,bg="cyan",borderwidth="10").pack()
    tkinter.Label(text="",bg="#FFA500").pack()
    tkinter.Button(text="Register", height="2", width="30", command=register,bg="cyan",borderwidth="10").pack()
    


    main_screen.mainloop()
main_account_screen()
try:
    global top
    top = tkinter.Tk()
    top.title("Chatter")
    top.configure(bg="#FFA500")

    global msg_list
    global my_msg

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent
    my_msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=20, width=100, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()
    entry_field = tkinter.Entry(top, textvariable=my_msg,width=40)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top,height=1,width=10, text="Send", bg="lime",font="arial" ,command=send)
    send_button["border"]="5"
    send_button.pack()
    send_button.pack()


    buttonExample = tkinter.Button(
            text="Chat history",bg="cyan",
            command=createChatHistory)
    buttonExample["border"]="5"
    buttonExample.pack()



    top.protocol("WM_DELETE_WINDOW", on_closing)

                        #----Now comes the sockets part----

    global client_socket
    global receive_thread

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((IP,int(PORT)))
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()
except ConnectionRefusedError:
    error=tkinter.Toplevel(top)
    error.configure(bg="#FFA500")
    error.title("ERROR")
    tkinter.Label(error, text="Server Not Online",justify='center',fg="Red").pack()
    error.mainloop()
    
