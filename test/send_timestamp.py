from time import time


import time

while True:
    with open("send_cache.txt", 'w') as f:
        f.write(str(time.time()))
    time.sleep(0.01)


