import threading
import socket
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
s = socket.socket()
s.bind((HOST,PORT))
s.listen(5)
print(f'Listening || 103.51.2.246, Local IP: {HOST} || {PORT}')

Message_cache = []
Clients = []
Nicknames = []


def recv_conn():
    print('Listening . . . ')
    conn, address = s.accept()
    print(f'Connection has been established | IP:{address[0]} | PORT:{address[1]}')
    Clients.append(conn)
    
    
    nickname_q = threading.Thread(target = ask_nick, args = (conn,))
    nickname_q.start()

def ask_nick(conn):

    recv_again = threading.Thread(target=recv_conn) 
    recv_again.start()

    conn.send(str.encode('Insert Nickname'))
    Nickname = str(conn.recv(1024),'utf-8')
    Nicknames.append(Nickname +str(Clients.index(conn)))

    for client in Clients:
        client.send(str.encode(f'{Nickname} has joined us nibbas'))


    if len(Message_cache) > 0:
        for msg in Message_cache:
            conn.send(str.encode(msg))
            time.sleep(0.07)
        
    # start a thread of recv message
    receive_msg = threading.Thread(target= recv_msg, args= (conn,))
    receive_msg.start()

def broadcast(message):
    pass

def recv_msg(Connection):
    while True:
        msg = str(Connection.recv(1024),"utf-8")

        for name in Nicknames:
            if int(name[-1]) == int(Clients.index(Connection)):
                nick = name
                break

        msg_brd = (f'{nick}: {msg}')
        Message_cache.append(msg_brd)
        print(msg_brd)
        
        for client in Clients:
            client.send(str.encode(msg_brd))
        
        if msg == 'gtg':
            time.sleep(0.1)
            Connection.close()
            print(f'{nick} has been disconnected')
            break


recv_conn()