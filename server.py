import socket
import threading

FORMAT = 'utf-8'
HEADER =1024
PORT = 3001
IP = "192.168.1.16"
ADDR=(IP, PORT)

global online_peers
online_peers = []


thread_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_peer_connection(conn, addr):
  thread_lock.acquire()
  username = conn.recv(1024).decode(FORMAT)
  conn.send(f"{username} connected".encode(FORMAT))
  
  online_user = (username, addr, conn)
  online_peers.append(online_user)
  
  global online_peers_status
  online_peers_status = True
  thread_lock.release()

def broadcast():
  server.listen()
  print(f"[LISTENING] Server is listening on {IP}")
  while True:
    conn, addr = server.accept()
    peer_thread = threading.Thread(target=handle_peer_connection, args=(conn, addr))
    peer_thread.start()
    peer_thread.join()
    if (online_peers_status):
      online_peers_names = []
      for peer in online_peers:
        online_peers_names.append(peer[0])
      print(f"ACTIVE: {online_peers_names}")
      for peer in online_peers:
        peer[2].send(str(online_peers_names).encode(FORMAT))
      
    
broadcast()
