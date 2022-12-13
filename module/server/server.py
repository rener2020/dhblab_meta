import socket
import threading
import json
from tkinter.messagebox import NO

from django.db import connection
from module.util import chaos2order


class Server:
    """
    服务器类
    """

    def __init__(self, ip, port):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connections = dict()

        self.ip = ip
        self.port = port

    def __user_thread(self, name):
        """
        用户子线程
        :param name: 用户id
        """
        connection = self.__connections[name]
        print('[Server] 用户', name, '加入系统')
        self.__broadcast("system",message='用户 '+
                         '(' + str(name) + ')' + '加入系统')

        # 侦听
        #
        last_broken_head = None
        while True:
            buffer = connection.recv(1024).decode()
            if not buffer:
                # 客户端断开
                if self.__connections[name]:
                    self.__connections[name].close()
                    self.__connections[name] = None
                print('[Server] 连接失效:', name, name)
                return
            # 解析成json数据
            order, broken_head, broken_tail = chaos2order(buffer, '{', '}')
            if last_broken_head and broken_tail:
                order.insert(0, last_broken_head + broken_tail)
            last_broken_head = broken_head

            for packet in order:
                try:
                    obj = json.loads(packet)
                    print(obj)
                except Exception:
                    continue
                # 如果是广播指令
                if obj['type'] == 'broadcast':
                    print(obj)
                    self.__broadcast(obj['name'], obj['message'])
                    continue
                # 如果是广播指令
                if obj['type'] == 'unicast':
                    self.__unicast(obj['target_name'],
                                   obj['sender_id'], obj['message'])
                    continue
                if obj['type'] == 'logout':
                    print('[Server] 用户', name, name, '退出系统')
                    self.__broadcast(message='用户 ' + str(name) +
                                     '(' + str(name) + ')' + '退出系统')
                    self.__connections[name].close()
                    self.__connections[name] = None
                    self.__names[name] = None
                    break
                print("+++++++++++")
                print('[Server] 无法解析json数据包:{}'.format(packet),
                    connection.getsockname(), connection.fileno())
                continue
                    

    def __unicast(self, target_name, name, message=''):
        """
        单播
        :param name: 用户id(0为系统)
        :param message: 广播内容
        """
        if target_name == name:
            return
        if target_name in self.__connections and self.__connections[target_name]:
            connection = self.__connections[target_name]
        else:
            print("目标不存在，sender:{},target:{}".format(name, target_name))
            return
        try:
            connection.send(json.dumps({
                'sender_name': name,
                'message': message
            }).encode())
        except Exception as e:
            print(e)
            print("连接错误，已断开:sender:{},target:{}".format(name, target_name))
            del self.__connections[target_name]

    def __broadcast(self, name, message=''):
        """
        广播
        :param name: 用户id(0为系统)
        :param message: 广播内容
        """
        print(message)
        for client_name in self.__connections:
            if name != client_name and self.__connections[client_name]:
                try:
                    self.__connections[client_name].send(json.dumps({
                        'sender_name': name,
                        'message': message
                    }).encode())
                except Exception as e:
                    print(name, 'dead')
                    print(e)
                    self.__connections[name] = None

    def __waitForLogin(self, connection):
        # 尝试接受数据
        # noinspection PyBroadException
        # try:
        buffer = connection.recv(1024).decode()
        # 解析成json数据
        obj = json.loads(buffer)
        # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
        if obj['type'] == 'login':
            self.__connections[obj['name']] = connection
            connection.send(json.dumps({
                'id': len(self.__connections) - 1
            }).encode())

            # 开辟一个新的线程
            thread = threading.Thread(
                target=self.__user_thread, args=(obj['name'],))
            thread.setDaemon(True)
            thread.start()
        else:
            print('[Server] 无法解析json数据包:',
                    connection.getsockname(), connection.fileno())
        # except Exception:
        #     print('[Server] 无法接受数据:', connection.getsockname(),
        #           connection.fileno())

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
        self.__connections["system"] = None

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] 收到一个新连接', connection.getsockname(),
                  connection.fileno())

            thread = threading.Thread(
                target=self.__waitForLogin, args=(connection,))
            thread.setDaemon(True)
            thread.start()
