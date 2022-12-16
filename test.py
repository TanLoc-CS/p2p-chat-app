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

# find = input()

# ls = [('talu', ('192.168.1.16', 44024)), ('mita', ('192.168.1.16', 51716)), ('as', ('192.168.1.16', 36462))]

# # for user in ls:
# #   if find in user:
# #     print("yes")
# #   else:
# #     print("no")

# print(str(ls).encode('utf-8'))

# def f1():
#   global _x
#   _x = 1
#   print(_x)
  
# def f2():
#   global _x
#   _x = 3
  
# f1()
# f2()
# print(_x)

# ls = [(1,'a'), (2,'b'), (3,'c')]
# ls1 = [(1,'a'), (2,'b'),(3,'c')]
# print(ls == ls1)

# for item in ls:
#   if 'b' in item:
#     idx = ls.index(item)
#     del ls[idx]
#     break
  
# print(ls)

msg = "('192.168.1.16', 37458)"

def regex_addr(msg):
  regex = msg[2:len(msg)-1].split("', ")
  return (regex[0], 12345)

print(regex_addr(msg))