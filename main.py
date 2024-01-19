import socket
import threading
import tkinter as tk
import time
import random


class Application:

    def __init__(self):
        self.userID = random.randint(10000, 99999)
        self.running = True

        self.currentMessage = ""
        self.messageStack = []
        self.sendMessageStack = []

        self.window = tk.Tk()
        self.window.title("John Message")
        self.window.configure(background='dark gray')

        self.userInputVar = tk.StringVar()

        self.chatDisplay = None
        self.scroll_y = None
        self.userInputBox = None
        self.sendButton = None
        self.server = None
        self.client = None

        self.launchComponents()

        socket.setdefaulttimeout(0.01)
        thread = threading.Thread(target=(lambda: self.launchConnection()))
        thread.start()

        # thread.join()

        # self.launchComponents()
        # self.launchConnection()
        def test():
            # print(len(self.messageStack))
            self.launchChatUpdateChecker()

            while (len(self.messageStack) > 0):
                newMessage = self.messageStack.pop()
                self.chatDisplay.configure(state="normal")
                self.chatDisplay.insert(tk.END, f"\n<Other> {newMessage}")
                self.chatDisplay.configure(state="disabled")

                self.chatDisplay.see("end")

            self.window.after(1, test)  # run this function again 2,000 ms from now

            while len(self.sendMessageStack) > 0:
                newMessage = self.sendMessageStack.pop()
                try:
                    self.client.send((newMessage).encode())
                except:
                    pass

        test()

        self.window.mainloop()

    def launchConnection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 4040))
        except:
            print("<ERROR> Failed To Connect TO Server.")
            print("(hint: Please Make Sure Your Server Is Running)")
            return

        # thread2 = threading.Thread(target=(lambda: self.launchChatUpdateChecker()))
        # thread2.start()
        # self.launchChatUpdateChecker()

    def launchComponents(self):
        self.scroll_y = tk.Scrollbar(self.window)
        self.chatDisplay = tk.Text(self.window, width=23, height=9, relief='groove', wrap='word',
                                   font=('arial', 25), yscrollcommand=self.scroll_y.set, background="dark gray")

        self.chatDisplay.insert(tk.END, f"Start of your conversation!")
        self.chatDisplay.configure(state="disabled")

        userInputBox = tk.Entry(self.window, textvariable=self.userInputVar, width=24, relief='groove',
                                font=('arial', 20), background="dark gray")

        def callback():
            self.onSend()
            userInputBox.delete(0, tk.END)

        def func(event):
            callback()

        self.window.bind('<Return>', func)

        sendButton = tk.Button(self.window, text="Send", command=callback)

        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.chatDisplay.pack(fill=tk.X)
        userInputBox.pack(side=tk.LEFT)
        sendButton.pack(side=tk.RIGHT)

        self.scroll_y.config(command=self.chatDisplay.yview)

    def launchChatUpdateChecker(self):
        # self.client.send(("RECEIVED").encode())
        # while True:
        if (self.client is not None):
            try:
                from_server = self.client.recv(4096)
                message = from_server.decode()
                print(message)
                # thread = threading.Thread(target=(lambda: receive()))
                # thread.start()
                if (message != ""):
                    self.messageStack.append(message)
            except Exception as exception:
                pass
        # threading.Timer(1, (lambda: self.launchChatUpdateChecker())).start()

    def onSend(self):
        userInput = self.userInputVar.get()
        if (userInput == '' or userInput == ' '): return

        self.chatDisplay.configure(state="normal")
        self.chatDisplay.insert(tk.END, "\n<You> " + userInput)
        self.chatDisplay.configure(state="disabled")

        self.sendMessageStack.append(userInput)


        self.chatDisplay.see("end")


application = Application()
