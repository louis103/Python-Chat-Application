import socket,threading

from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 9999

class Client_GUI:
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))
        msg = Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname","Please add a nickname",parent=msg)
        self.gui_build_success = False
        self.gui_running = True

        gui_thread = threading.Thread(target=self.gui_build)
        receiver_thread = threading.Thread(target=self.receive_server)

        gui_thread.start()
        receiver_thread.start()

    def gui_build(self):
        self.root = Tk()
        self.root.config(bg="white")

        self.chat_label = Label(self.root,text="Chat App",font=("Arial",16),bg="white")
        self.chat_label.pack(pady=5,padx=20)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.root)
        self.text_area.pack(pady=8,padx=20)
        self.text_area.config(state=DISABLED)

        self.msg_label = Label(self.root, text="Message", font=("Arial", 12), bg="white")
        self.msg_label.pack(pady=5, padx=20)

        self.input_area = Text(self.root,height=3)
        self.input_area.pack(padx=20,pady=5)

        self.send_btn = Button(self.root,text="Send",font=("Arial",12),bg="white",command=self.send)
        self.send_btn.pack(padx=20,pady=5)

        self.gui_build_success = True
        self.root.protocol("WM_DELETE_WINDOW",self.stop)
        self.root.mainloop()

    def send(self):
        message = f"{self.nickname}: {self.input_area.get(1.0,END)}"
        self.sock.send(message.encode("utf-8"))
        self.input_area.delete(1.0,END)

    def stop(self):
        self.gui_running = False
        self.root.destroy()
        self.sock.close()
        exit(0)

    def receive_server(self):
        while self.gui_running:
            try:
                message = self.sock.recv(2048).decode("utf-8")
                if message == "NICKNAME":
                    self.sock.send(self.nickname.encode("utf-8"))
                else:
                    if self.gui_build_success:
                        self.text_area.config(state=NORMAL)
                        self.text_area.insert(END,message)
                        self.text_area.yview(END)
                        self.text_area.config(state=DISABLED)
            except ConnectionAbortedError:
                break
            except Exception as err:
                print(f"Error, {err}")
                self.sock.close()
                break

client = Client_GUI(HOST,PORT)

