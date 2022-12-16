import socket
import threading

FORMAT = 'utf-8'
HEADER =1024
PORT = 3002
IP = '192.168.1.16'
ADDR=(IP, PORT)

online_users = []

lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def regex_addr(msg):
  regex = msg[2:len(msg)-1].split("', ")
  return (regex[0], 12345)


def broadcast():
  try:
    global online_users
    online_client_names = []
    for user in online_users:
      online_client_names.append(user[0])
    print(f'ACTIVE: {online_client_names}')
    for client in online_users:
      client[1].send(str(online_client_names).encode(FORMAT))
  except:
    return 1

def handle_client(conn, addr):
  try: 
    connected = True
    
    while connected:
      global online_users
      msg = conn.recv(1024).decode(FORMAT)
      
      if (str(msg).startswith('@')):
        lock.acquire()
        peer = msg[3:len(msg)-1].split("', ")
        online_user = (peer[0], conn, peer[1][1:len(peer[1])], int(peer[2]))
        online_users.append(online_user)
        lock.release()
        broadcast()
      elif (str(msg).startswith('$')):
        found = 'NOT FOUND!'
        find = msg.split('$')[1]
        for user in online_users:
          if find in user:
            print((user[2], user[3]))
            found = str((user[2], user[3])).encode(FORMAT)
            conn.send(found)
        if (found == 'NOT FOUND!'):
          conn.send(found.encode(FORMAT))
      elif (str(msg) == 'disconnect'):
        lock.acquire()
        for user in online_users:
          if addr[0] in user:
            idx = online_users.index(user)
            print(f'{user[0]} disconnected.')
            del online_users[idx]
        lock.release()
        conn.send('disconnected'.encode(FORMAT))
        conn.close()
        broadcast()
      else:
        conn.send('Cmd error...'.encode(FORMAT))
  except:
    return 1


def start(): 
  try:
    server.listen()
    print(f'[LISTENING] Server is listening on {IP}')
    while True:
      conn, addr = server.accept()
      client_thread = threading.Thread(target=handle_client, args=(conn, addr))
      client_thread.start()
  except:
    return 1

start()