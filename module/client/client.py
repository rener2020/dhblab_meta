import socket
import threading
import json
import time
import os

from regex import F
from module.util import chaos2order
from module.file import get, put


class Client():
    """
    客户端
    """
    prompt = ''
    intro = '[Welcome] 简易系统客户端(Cli版)\n' + '[Welcome] 输入help来获取帮助\n'

    def __init__(self, ip, port, name):
        """
        构造
        """
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        # ！！！！！！！！！！！！
        # 在这里配置你的机器用户名，使用英文字母（数字）
        self.__nickname = name
        self.__is_login = False
        self.__connected = False

        self.ip = ip
        self.port = port

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        last_broken_head = None
        while self.__is_login:
            # noinspection PyBroadException
            try:
                buffer = self.__socket.recv(1024).decode()
            except Exception as e:
                print("通讯异常，程序终止")
                self.__connected = False
                return
            if not buffer:
                # 服务端断开
                print("通讯异常，程序终止")
                self.__connected = False
                return

            order, broken_head, broken_tail = chaos2order(buffer, '{', '}')
            if last_broken_head and broken_tail:
                order.insert(0, last_broken_head + broken_tail)
            last_broken_head = broken_head

            for packet in order:
                info = json.loads(packet)

                if 'sender_nickname' not in info:
                    print("数据包异常，数据包为：", packet)
                    continue

                file_path = "./storage/devices/_{}.txt".format(
                    info['sender_nickname'])
                put(packet, file_path)
                print(packet)

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        try:
            self.__socket.send(json.dumps({
                'type': 'broadcast',
                'sender_id': self.__id,
                'message': message
            }).encode())
        except Exception as e:
            print(e)
            self.__connected = False

    def connect(self):
        try:
            self.__socket.connect((self.ip, self.port))
            return True
        except Exception as e:
            pass
        return False

    def start(self):
        """
        启动客户端
        """
        while True:
            print('正在连接到服务器...')
            # 第一次连接
            self.__connected = self.connect()
            if self.__connected:
                # 如果已连接上
                break
            else:
                time.sleep(1)
                    

        while True:
            # 连接
            if not self.__connected:
                print('连接断开，正在重连...')
                # 未连接，则重置登录状态
                self.__is_login = False
                self.__socket.close()
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__connected = self.connect()
            if not self.__connected:
                time.sleep(1)
                continue



            if not self.__is_login:
                
                # 用户登录
                self.login()
                if self.__is_login:
                    # 如果登录成功
                    # 开启子线程用于接受数据
                    thread = threading.Thread(
                        target=self.__receive_message_thread)
                    thread.setDaemon(True)
                    thread.start()
                else:
                    # 登录失败，等待一秒
                    time.sleep(1)
                    continue
            for i in range(4):
                path = './storage/devices/self_{}.txt'.format(i)
                if os.path.exists(path):
                    self.send(get(path))
            # 数据更新频率在这里控制
            time.sleep(0.01)

    def login(self):
        """
        登录系统
        :param args: 参数
        """
        # 将昵称发送给服务器，获取用户id
        self.__socket.send(json.dumps({
            'type': 'login',
            'nickname': self.__nickname
        }).encode())
        # 尝试接受数据
        # noinspection PyBroadException
        try:
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            if obj['id']:
                self.__id = obj['id']
                # 登录成功
                self.__is_login = True
                print('[Client] 成功登录到系统')
            else:
                print('[Client] 无法登录到系统')
        except Exception:
            print('[Client] 无法从服务器获取数据')

    def send(self, message):
        """
        发送消息
        :param args: 参数
        """
        # 显示自己发送的消息
        # print('[' + str(self.__nickname) +
        #     '(' + str(self.__id) + ')' + ']', message)
        # 开启子线程用于发送数据
        thread = threading.Thread(
            target=self.__send_message_thread, args=(message,))
        thread.setDaemon(True)
        thread.start()

    def logout(self, args=None):
        """
        登出
        :param args: 参数
        """
        self.__socket.send(json.dumps({
            'type': 'logout',
            'sender_id': self.__id
        }).encode())
        self.__is_login = False
        return True
