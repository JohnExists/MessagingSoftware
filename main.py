import socket
import threading
import tkinter as tk


class Application:

    def __init__(self):
        # The messages sent to and from the other peroson
        self.messageStack = []

        # Initializes the window and tkinter
        self.window = tk.Tk()
        self.window.title("John Message")
        self.window.configure(background='dark gray')
        self.window.resizable(False, False)

        # The variable for whatever the user typed into menu
        self.userInputVar = tk.StringVar()

        # Setting up all the components of the window
        self.chatDisplay = None
        self.scroll_y = None
        self.userInputBox = None
        self.sendButton = None
        self.server = None
        self.client = None

        # Initializing all these components
        self.launchComponents()

        # Setting up the connection to the server
        socket.setdefaulttimeout(0.01)
        thread = threading.Thread(target=(lambda: self.launchConnection()))
        thread.start()

        # Loads any unread messages from the other person
        def loadOthersMessages():
            # Checks if theres any messages received from the other person
            self.launchChatUpdateChecker()

            # If there is a message available
            while (len(self.messageStack) > 0):
                # Remove it from the list and display it
                newMessage = self.messageStack.pop()
                self.chatDisplay.configure(state="normal")
                self.chatDisplay.insert(tk.END, f"\n<Other> {newMessage}")
                self.chatDisplay.configure(state="disabled")

                self.chatDisplay.see("end")
            # Call this function again after 1 ms
            self.window.after(1, loadOthersMessages)

        loadOthersMessages()

        # Sets up the window close event and starts the main loops
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
        self.window.mainloop()

    def launchConnection(self):
        # Attempts to connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 4040))
        except:
            # If no server is found :(
            print("<ERROR> Failed To Connect TO Server.")
            print("(hint: Please Make Sure Your Server Is Running)")
            return

    def launchComponents(self):
        # Initializes the scrollbar
        self.scroll_y = tk.Scrollbar(self.window)
        # Initializes the chat display
        self.chatDisplay = tk.Text(self.window, width=23, height=9, relief='groove', wrap='word',
                                   font=('arial', 25), yscrollcommand=self.scroll_y.set, background="dark gray")
        self.chatDisplay.insert(tk.END, f"Start of your conversation!")
        self.chatDisplay.configure(state="disabled")

        userInputBox = tk.Entry(self.window, textvariable=self.userInputVar, width=24, relief='groove',
                                font=('arial', 20), background="dark gray")

        # Functions are called when the user press the "Enter" key 
        # or clicks the "Send" button
        def callback():
            self.onSend()
            userInputBox.delete(0, tk.END)

        def func(event):
            callback()

        self.window.bind('<Return>', func)

        # Initializes the "Send" button
        sendButton = tk.Button(self.window, text="Send", command=callback)

        # Places all the components in the right place
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.chatDisplay.pack(fill=tk.X)
        userInputBox.pack(side=tk.LEFT)
        sendButton.pack(side=tk.RIGHT)

        self.scroll_y.config(command=self.chatDisplay.yview)

    def launchChatUpdateChecker(self):
        # Checks if theres any messages received from the other person
        if (self.client is not None):
            try:
                # Sends something to receive something back
                self.client.send(("RECEIVED").encode())
                # Reads the message from server
                from_server = self.client.recv(4096)
                message = from_server.decode()
                # If there is a message append it to the message Stack
                if (message != ""):
                    self.messageStack.append(message)
            except Exception as exception:
                pass

    def onSend(self):
        # Gets the input from the user
        userInput = self.userInputVar.get()
        if (userInput == '' or userInput == ' '): return

        # Adds the users message to the chat
        self.chatDisplay.configure(state="normal")
        self.chatDisplay.insert(tk.END, "\n<You> " + userInput)
        self.chatDisplay.configure(state="disabled")

        # Sends the input to the server
        try:
            self.client.send((userInput).encode())
        except:
            pass


        self.chatDisplay.see("end")

    def on_closing(self):
        # Closes the application
        self.window.destroy()
        self.client.close()

application = Application()
