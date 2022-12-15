import socket
import threading

HEADER = 1024
PORT = 3001
FORMAT = 'utf-8'
IP = '192.168.1.16'
ADDR = (IP, PORT)

server_connected = False
connecting_peer_addr = ''

lock = threading.Lock()

def request_server(client):
  try:
    while server_connected:
      msg = input()
      client.send(msg.encode(FORMAT))
  except:
    print('[ERR] Error in request_server()...')



def handle_response(client):
  try:
    global server_connected
    while server_connected:
      msg = client.recv(1024).decode(FORMAT)
      if (msg == 'disconnected'):
        lock.acquire()
        print(msg + '\nPress Enter to exit...')
        server_connected = False
        lock.release()
      elif(str(msg).startswith('(')):
        global connecting_peer_addr
        connecting_peer_addr = msg
        print(f'[CONNECTING PEER] peer: {connecting_peer_addr}')
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

def start():
  try:
    connect_server_thread = threading.Thread(target=connect_server, args=())
    connect_server_thread.start()
  except:
    print('[ERR] Error in start()...')
    
start()