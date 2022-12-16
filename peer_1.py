import socket
import threading
import time

HEADER_LENGTH = 1024
FORMAT = 'utf-8'

IP = '192.168.1.16'
PORT = 3002
ADDR = (IP, PORT)

# PEER_IP = socket.gethostbyname(socket.gethostname())
PEER_IP = '192.168.1.16'
PEER_PORT = 12345
PEER_ADDR = (PEER_IP, PEER_PORT)

server_connected = False
peer_connected = False
connecting_peer_addr = ''

lock = threading.Lock()

### Connect to main server ###
def request_server(client):
  try:
    while server_connected:
      if not peer_connected:
        msg = input()
        client.send(msg.encode(FORMAT))
  except:
    print('[ERR] Error in request_server()...')


def handle_response(client):
  try:
    global server_connected
    while server_connected:
      msg = client.recv(HEADER_LENGTH).decode(FORMAT)
      if (msg == 'disconnected'):
        print(msg + '\n\nPress Enter to exit...')
        server_connected = False
      elif(str(msg).startswith('(')):
        global connecting_peer_addr
        connecting_peer_addr = msg
        print(f'[CONNECTING PEER] peer: {connecting_peer_addr}')
        global peer_connected
        peer_connected = True
        print('Press Enter to start chat...')
      elif(str(msg).startswith('[')):
        print(f'[ACTIVE PEERS]: {msg}')
      else:
          print(f'[ACTIVE PEERS]{msg}')
  except:
    print('[ERR] Error in handle_response()...')


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
    print('[ERR] Error in connect_server()...')
###############################################

### Connect to peer server ###
def regex_addr(msg):
  regex = msg[2:len(msg)-1].split("', ")
  return (regex[0], 54321)


# def send_msg(client):
#   try:
#     connected = True
#     while connected:
#       msg = input('You: ')
#       encoded_msg = msg.encode(FORMAT)
#       msg_length = str(len(encoded_msg)).encode(FORMAT)
#       msg_length += b' ' * (HEADER_LENGTH - len(msg_length))
#       client.send(msg_length)
#       client.send(encoded_msg)
#   except:
#     print('[ERR] Error in send_msg()...')


def connect_peer():
  try:
    global peer_connected
    while server_connected:
      if peer_connected:
        global connecting_peer_addr
        peer_addr = regex_addr(connecting_peer_addr)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(peer_addr)
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
    print('[ERR] Error in connect_peer()...')
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
    print('[ERR] Error in handle_peer()...')


def start_peer_server():
  try:
    peer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_server.bind(PEER_ADDR)
    peer_server.listen()
    print(f'[LISTENING] PEER is listening on {peer_server.getsockname()}')
    while True:
      conn, addr = peer_server.accept()
      if addr:
        print(f'in p_s {addr}')
      peer_thread = threading.Thread(target=handle_peer, args=(conn, addr))
      peer_thread.start()
  except:
    print('[ERR] Error in start_peer_server()...')
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
    print('[ERR] Error in start()...')
    
start()