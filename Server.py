import socket
import pathlib
from pathlib import Path
import os


class Server:

    def __init__(self):

        self.host = socket.gethostname()
        self.port = 5000  # initiate port no above 1024
        print("Host Name: "+self.host)

        self.server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind((self.host, self.port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        self.server_socket.listen(2)
        self.conn, self.address = self.server_socket.accept()  # accept new connection
        print("Connection from: " + str(self.address))

    def action(self):
        action = self.conn.recv(1024).decode().lower()
        return action

    def send_path_names(self):

        p = Path(r'Server').glob('**/*')
        files = [x for x in p if x.is_file()]
        files_string = []
        for x in files:
            files_string.append(str(x.name))
        self.conn.send(','.join(files_string).encode())
        print("Server: Files Has Been Sent")

    def download(self, file_name: str):

        server_path = "Server/" + file_name
        file_size = str(os.path.getsize(server_path))
        self.conn.send(file_size.encode())
        if self.conn.recv(1024).decode() == "size":
            f = open(server_path, "rb")
            while True:
                file_data = f.read(1024)
                self.conn.send(file_data)
                if len(file_data) == 0:
                    f.close()
                    break
            print("Server: The File Uploded To Client")

    def upload(self, file_name):
        c = open("Server/"+file_name, "x")
        c.close()
        file_size = int(self.conn.recv(1024).decode())
        self.conn.send("size".encode())
        f = open("Server/"+file_name, "wb")
        while True:
            file_data = self.conn.recv(1024)
            f.write(file_data)
            file_size -= 1024
            if file_size <= 0:
                f.close()
                print("Server: Client Add File To The Server")
                break


def main():
    s = Server()
    while True:
        action = s.action()
        print("Client Action: "+action)
        if action == "download":
            s.send_path_names()
            s.download(s.conn.recv(1024).decode())
        if action == "upload":
            file_name = s.conn.recv(1024).decode()
            s.upload(file_name)
        if action == "stop":
            s.conn.close()
            break


main()
