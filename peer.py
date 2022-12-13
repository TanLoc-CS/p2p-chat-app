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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

username = input("Enter username: ")
client.connect(ADDR)


def connect_to_server():
  client.send(username.encode(FORMAT))
  while True:
    try:
      msg = client.recv(1024).decode(FORMAT)
      print(f"ACTIVE PEER: {msg}")
    except:
        print("Error occur...")
        pass


connect_to_server_thread = threading.Thread(target=connect_to_server, args=())
connect_to_server_thread.start()
connect_to_server_thread.join()