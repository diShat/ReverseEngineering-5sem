import socket
import os
import subprocess

client = socket.socket()
client_ip = socket.gethostbyname(socket.gethostname())

client.connect((client_ip, 12284))

print('Connection: Success!')

client.send('Client connected succesfully'.encode())

if os.name == 'posix':
    info = (subprocess.getoutput('lscpu')).encode()
    client.send(info)
    print('Data sent..')

client.close()
print('Disconnected.')