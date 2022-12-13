# def handle_msg(msg):
#   encoded_msg = msg.encode(FORMAT)
#   msg_length = str(len(encoded_msg)).encode(FORMAT)
#   msg_length += b' ' * (HEADER - len(msg_length))
#   client.send(msg_length)
#   client.send(encoded_msg)
import socket
import threading

HEADER = 1024
PORT = 3001
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.16"
ADDR = (SERVER, PORT)

thread_lock = threading.Lock()

connected_server = False

connecting_peer_addr = ""

def send_cmd(client):
  cmd = input()
  client.send(cmd.encode(FORMAT))

def receive(client):
  msg = client.recv(1024).decode(FORMAT)
  return msg

def cli_to_server(client):
  global connected_server
  global connecting_peer_addr
  
  while connected_server:
    send_thread = threading.Thread(target=send_cmd, args=(client,))
    send_thread.start()
    recieved_msg = receive(client)
    if (recieved_msg == "disconnected"):
      print(recieved_msg)
      connected_server = False
    elif(str(recieved_msg).startswith('(')):
      connecting_peer_addr = recieved_msg
      print(f"[CONNECTING PEER] peer: {connecting_peer_addr}")


def observe_server(client):
  while connected_server:
    online_peers = receive(client)
    if (str(online_peers).startswith('[')):
      print(f"[ACTIVE PEERS]: {online_peers}")
    


def connect_server():
  username = input("Enter username: ")
  
  thread_lock.acquire()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(ADDR)
  global connected_server
  connected_server = True
  client.send(username.encode(FORMAT))
  thread_lock.release()
  
  observe_server_thread = threading.Thread(target=observe_server, args=(client,))
  cli_to_server_thread = threading.Thread(target=cli_to_server, args=(client,))
  observe_server_thread.start()
  cli_to_server_thread.start()  

def start():
  connect_to_server_thread = threading.Thread(target=connect_server, args=())
  connect_to_server_thread.start()
  pass


start()