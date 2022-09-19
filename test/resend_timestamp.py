import time
import json

while True:
    with open("recv_cache.txt", 'r') as f1:
        timestamp = json.loads(f1.read().split("}")[0]  + "}")['message']
        with open("send_cache.txt", 'w') as f2:
            f2.write(timestamp)
    time.sleep(0.01)
