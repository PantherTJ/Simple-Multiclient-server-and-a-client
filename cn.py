import socket
import time
import threading

# ASK for IP
print('Please enter the ip')
host = input()

port = 9999
sock = socket.socket()

sock.connect((host,port))

def rec_msg():
    while True:
        msg = sock.recv(1024).decode('utf-8')
        print(msg)

def send_msg():
    while True:
        msg = input()
        
        if msg == 'gtg':
            sock.send(str.encode(msg))
            time.sleep(2)
            break
        else:
            sock.send(str.encode(msg))
        



send = threading.Thread(target = send_msg)
receive = threading.Thread(target= rec_msg)

send.start()
receive.start()

send.join()
receive.join()