import socket
import pathlib
from pathlib import Path
import os


def create_file(path_location, file_name):
    f = open(path_location + "/" + file_name, "x")
    f.close()


class Client:

    def __init__(self):

        self.host = socket.gethostname()  # as both code is running on same pc
        self.port = 5000  # socket server port number

        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((self.host, self.port))  # connect to the server

    def server_file_print(self):
        files = self.client_socket.recv(1024).decode()
        files_list = files.split(",")
        i = 1
        for x in files_list:
            print("File "+str(i)+" : ["+x+"]")
            i += 1
        return files_list

    def download(self, file_path):
        f = open(file_path, "wb")
        file_size = int(self.client_socket.recv(1024).decode())
        self.client_socket.send("size".encode())
        while True:
            file_data = self.client_socket.recv(1024)
            f.write(file_data)
            file_size -= 1024
            if file_size <= 0:
                f.close()
                print("Client: Files Downloaded")
                break

    def upload(self, path_file: str):
        f = open(path_file, "rb")
        file_size = str(os.path.getsize(path_file))
        self.client_socket.send(file_size.encode())
        if self.client_socket.recv(1024).decode() == "size":
            while True:
                file_data = f.read(1024)
                self.client_socket.send(file_data)
                if len(file_data) == 0:
                    f.close()
                    break


def main():

    c = Client()
    action_list = ["upload", "download", "stop"]
    while True:
        while True:
            action = str(input("Enter Action: "))
            if action in action_list:
                c.client_socket.send(action.encode())
                break
        if action == "download":
            fl = c.server_file_print()

            while True:
                file_name = str(input("Enter File Name: "))
                if file_name in fl:
                    c.client_socket.send(file_name.encode())
                    break
            create_file("Recive", file_name)
            c.download(str("Recive/"+file_name))
            print("File Downloaded")

        if action == "upload":
            path_location = str(input("Enter Path Location: "))
            path = Path(path_location).name
            c.client_socket.send(path.encode())
            c.upload(path_location)

        if action == "stop":
            c.client_socket.close()
            break


main()