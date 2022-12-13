# import threading

# lock = threading.Lock()

# global ls
# ls = []

# def handle_connect(id:int):
#   lock.acquire()
#   ls.append(id)
#   lock.release()

# def start(id):
#   thread = threading.Thread(target=handle_connect, args=(id,))
#   thread.start()
#   thread.join()
  
# start(1)
# start(2)
# start(3)

# print(ls)

find = input()

ls = [('talu', ('192.168.1.16', 44024)), ('mita', ('192.168.1.16', 51716)), ('as', ('192.168.1.16', 36462))]

# for user in ls:
#   if find in user:
#     print("yes")
#   else:
#     print("no")

print(str(ls).encode('utf-8'))