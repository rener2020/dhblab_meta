from time import time
import time

while True:
    with open("recv_cache.txt", 'r') as f:
        print("pre",f.read())
        print("cur",time.time())
    time.sleep(0.01)
