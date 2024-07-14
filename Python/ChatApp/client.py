import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Client():
    def __init__(self, window, host, port) -> None:
        self.window = window

        ## Define tkinter
        self.messageBox = tk.Listbox(window, height=20, width=100, bg="#fc6c85")
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg="#fc6c85", fg="#000000")
        self.msgEntry.pack()

        self.sendMsgButton = tk.Button(window, text="Send Message", width=50, bg="#fc6c85", command=self.sendTexts)
        self.sendMsgButton.pack()

        self.host = host
        self.port = port
        self.buffer = 1024
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        Thread(target=self.receiveTexts).start()

    def sendTexts(self):
        self.sock.send(bytes(self.msgEntry.get(), "utf8"))
        self.msgEntry.delete(0, 'end') ## Clears the entry field

    def receiveTexts(self):
        while True:
            try:
                msg = self.sock.recv(self.buffer).decode("utf8")
                self.messageBox.insert(tk.END, msg)
            except OSError:
                break

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chat Box")
    Client(window, "localhost", 8000)

    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
