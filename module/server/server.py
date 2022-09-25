import socket
import threading
import json
from module.util import chaos2order
from config.system import DEBUG

class Server:
    """
    服务器类
    """

    def __init__(self,ip,port):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connections = list()
        self.__nicknames = list()

        # 
        self.ip = ip
        self.port = port

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        connection = self.__connections[user_id]
        nickname = self.__nicknames[user_id]
        print('[Server] 用户', user_id, nickname, '加入系统')
        self.__broadcast(message={
            'sender_id': user_id,
            'sender_nickname': self.__nicknames[user_id],
            'message': '用户 ' + str(nickname) +
                         '(' + str(user_id) + ')' + '加入系统'
                         }
                         )

        # 侦听
        last_broken_head = None
        while True:
            buffer = connection.recv(1024).decode()
            if not buffer:
                # 客户端断开
                self.__connections[user_id].close()
                self.__connections[user_id] = None
                self.__nicknames[user_id] = None
                print('[Server] 连接失效:', user_id, nickname)
                return
            # 解析成json数据
            order, broken_head, broken_tail = chaos2order(buffer, '{', '}')
            if last_broken_head and broken_tail:
                order.insert(0, last_broken_head + broken_tail)
            last_broken_head = broken_head

            for packet in order:
                if DEBUG:
                    print(packet)
                obj = json.loads(packet)
                obj = json.loads(packet)
                # 广播全部
                self.__broadcast(user_id, obj)

    def __broadcast(self, user_id=0, message=''):
        """
        广播
        :param user_id: 用户id(0为系统)
        :param message: 广播内容
        """

        for i in range(1, len(self.__connections)):
            # print(len(self.__connections))
            # if self.__connections[i] is None:
            #     continue
            if user_id != i and self.__connections[i]:
                try:
                    self.__connections[i].send(json.dumps(message).encode())
                except Exception:
                    print(i, 'dead')
                    self.__connections[i] = None

    def __waitForLogin(self, connection):
        # 尝试接受数据
        # noinspection PyBroadException
        try:
            buffer = connection.recv(1024).decode()
            # 解析成json数据
            obj = json.loads(buffer)
            # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
            if obj['type'] == 'login':
                self.__connections.append(connection)
                self.__nicknames.append(obj['nickname'])
                connection.send(json.dumps({
                    'id': len(self.__connections) - 1
                }).encode())

                # 开辟一个新的线程
                thread = threading.Thread(
                    target=self.__user_thread, args=(len(self.__connections) - 1,))
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Server] 无法解析json数据包:',
                      connection.getsockname(), connection.fileno())
        except Exception:
            print('[Server] 无法接受数据:', connection.getsockname(),
                  connection.fileno())

    def start(self):
        """
        启动服务器
        """
        # 绑定端口
        self.__socket.bind((self.ip, self.port))
        # 启用监听
        self.__socket.listen(100)
        print('[Server] 服务器正在运行......')

        # 清空连接
        self.__connections.clear()
        self.__nicknames.clear()
        self.__connections.append(None)
        self.__nicknames.append('System')

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] 收到一个新连接', connection.getsockname(),
                  connection.fileno())

            thread = threading.Thread(
                target=self.__waitForLogin, args=(connection,))
            thread.setDaemon(True)
            thread.start()
