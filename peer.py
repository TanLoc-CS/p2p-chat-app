import socket
import threading
import random

HEADER_LENGTH = 1024
FORMAT = 'utf-8'

IP = '192.168.1.16'
PORT = 3002
ADDR = (IP, PORT)

# PEER_IP = socket.gethostbyname(socket.gethostname())
PEER_IP = '192.168.1.16'
PEER_PORT = random.randint(10000, 65000)
PEER_ADDR = (PEER_IP, PEER_PORT)

server_connected = False
peer_connected = False
connecting_peer = ''

lock = threading.Lock()

### Connect to main server ###
def request_server(client):
  try:
    while server_connected:
      if not peer_connected:
        global username
        msg = input()
        if (msg.startswith('@')):
          msg = '@' + str((msg.split('@')[1], PEER_IP, PEER_PORT))
        client.send(msg.encode(FORMAT))
  except:
    return 1


def handle_response(client):
  try:
    global server_connected
    while server_connected:
      msg = client.recv(HEADER_LENGTH).decode(FORMAT)
      if (msg == 'disconnected'):
        print(msg + '\n\nPress Enter to exit...')
        server_connected = False
      elif(str(msg).startswith('(')):
        global connecting_peer
        connecting_peer = msg
        print(f'[CONNECTING PEER] peer: {connecting_peer}')
        global peer_connected
        peer_connected = True
        print('Press Enter to start chat...')
      elif(str(msg).startswith('[')):
        print(f'[ACTIVE PEERS]: {msg}')
      else:
          print(f'[ACTIVE PEERS]{msg}')
  except:
    return 1


def connect_server():
  try: 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    global server_connected
    server_connected = True
    request_server_thread = threading.Thread(target=request_server, args=(client,))
    handle_response_thread = threading.Thread(target=handle_response, args=(client,))
    request_server_thread.start()
    handle_response_thread.start()
  except:
    return 1
###############################################

### Connect to peer server ###
def regex_addr(s):
  regex = s[2:len(s)-1].split("', ")
  return (regex[0], int(regex[1]))

def connect_peer():
  try:
    global peer_connected
    while server_connected:
      if peer_connected:
        global connecting_peer
        peer_addr = regex_addr(connecting_peer)
        print(peer_addr)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(peer_addr)
        connected = True
        while connected:
          msg = input()
          encoded_msg = msg.encode(FORMAT)
          msg_length = str(len(encoded_msg)).encode(FORMAT)
          msg_length += b' ' * (HEADER_LENGTH - len(msg_length))
          client.send(msg_length)
          client.send(encoded_msg)
          if (msg == 'exit'):
            peer_connected = False
  except:
    return 1
###############################################

### Create peer server ###
def handle_peer(conn, addr):
  try:
    print(addr)
    connected = True
    while connected:
      msg_length = conn.recv(HEADER_LENGTH).decode(FORMAT)
      if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == 'exit':
          print(f'{addr}: {msg}')
          conn.close()
          break
        else:
          print(f'{addr}: {msg}')
  except:
    return 1


def start_peer_server():
  try:
    peer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_server.bind(PEER_ADDR)
    peer_server.listen()
    print(f'[LISTENING] PEER is listening on {peer_server.getsockname()}')
    while True:
      conn, addr = peer_server.accept()
      peer_thread = threading.Thread(target=handle_peer, args=(conn, addr))
      peer_thread.start()
  except:
    return 1
###############################################

def start():
  try:
    connect_server_thread = threading.Thread(target=connect_server, args=())
    start_peer_server_thread = threading.Thread(target=start_peer_server, args=())
    connect_peer_thread = threading.Thread(target=connect_peer, args=())
    connect_server_thread.start()
    start_peer_server_thread.start()
    connect_peer_thread.start()
  except:
    return 1
    
start()