from ctypes import c_int
import socket

server = socket.socket()
server_ip = socket.gethostbyname(socket.gethostname())

server.bind((server_ip, 12284))
server.listen(1)
client, client_ip = server.accept()

mes = client.recv(1024).decode()
print("{}\tIP: {}".format(mes, client_ip))

with open("/home/kali/lab5/connection_data.txt", 'wb') as file:
    data = client.recv(2058)
    file.write(data)
    print("Data received.")

client.close()
print("Disconnected.")