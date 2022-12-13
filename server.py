import socket
import threading

FORMAT = 'utf-8'
HEADER =1024
PORT = 3001
IP = "192.168.1.16"
ADDR=(IP, PORT)

online_peers = []

online_peers_status = False

thread_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_connection(conn, addr):
  thread_lock.acquire()
  username = conn.recv(1024).decode(FORMAT)  
  online_user = (username, conn, addr)
  global online_peers
  online_peers.append(online_user)
  global online_peers_status
  online_peers_status = True
  thread_lock.release()

def handle_cmd(conn, addr):
  connected = True
  while connected:
    msg = conn.recv(1024).decode(FORMAT)
    if (msg == "disconnect"):
      thread_lock.acquire()
      global online_peers
      for peer in online_peers:
        if addr in peer:
          idx = online_peers.index(peer)
          del online_peers[idx]
      print(online_peers)
      global online_peers_status
      online_peers_status = True
      conn.send("disconnected".encode(FORMAT))
      conn.close()
      connected = False
      thread_lock.release()
    else:
      user = "NOT FOUND!"
      for peer in online_peers:
        if msg in peer:
          user = str(peer[2]).encode(FORMAT)
          conn.send(user)
      if (user == "NOT FOUND!"):
        conn.send(user.encode(FORMAT))


def handle_peer(conn, addr):
  connection_thread = threading.Thread(target=handle_connection, args=(conn, addr))
  connection_thread.start()
  connection_thread.join()
  cmd_thread = threading.Thread(target=handle_cmd, args=(conn, addr))
  cmd_thread.start()
  cmd_thread.join()
  print(f"{addr} disconnected.")


def broadcast():
  while True:
    global online_peers_status
    if (online_peers_status):
      online_peers_names = []
      thread_lock.acquire()
      for peer in online_peers:
        online_peers_names.append(peer[0])
      print(f"ACTIVE: {online_peers_names}")
      for peer in online_peers:
        peer[1].send(str(online_peers_names).encode(FORMAT))
      online_peers_status = False
      thread_lock.release()

def start(): 
  try:
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}")
    broadcast_thread = threading.Thread(target=broadcast,args=())
    broadcast_thread.start()
    while True:
      conn, addr = server.accept()
      peer_thread = threading.Thread(target=handle_peer, args=(conn, addr))
      peer_thread.start()
  except:
    return 0;

start()