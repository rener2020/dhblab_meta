import socket
import threading
import json
import time


class Client():
    """
    客户端
    """
    prompt = ''
    intro = '[Welcome] 简易系统客户端(Cli版)\n' + '[Welcome] 输入help来获取帮助\n'

    def __init__(self):
        """
        构造
        """
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        # ！！！！！！！！！！！！
        # 在这里配置你的机器用户名，使用英文字母（数字）
        self.__nickname = 'C4'
        self.__isLogin = False

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while self.__isLogin:
            # noinspection PyBroadException
            try:
                buffer = self.__socket.recv(1024).decode()
                with open('recv_cache.txt', 'w') as f:
                    # 将获取的信息写入文件中
                    f.write(str(buffer))
                # print('[' + str(obj['sender_nickname']) + '(' + str(obj['sender_id']) + ')' + ']', obj['message'])
            except Exception as e:
                print(e)
                print('[Client] 无法从服务器获取数据')

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())

    def start(self):
        """
        启动客户端
        """
        self.__socket.connect(('0.0.0.0', 8888))

        while True:
            if not self.__isLogin:
                # 用户登录
                self.login()
                if self.__isLogin:
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
            with open('send_cache.txt', 'r') as f:
                self.send(f.read().strip())
            # 数据更新频率在这里控制
            time.sleep(0.1)

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
                self.__isLogin = True
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
        #print('[' + str(self.__nickname) +
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
        self.__isLogin = False
        return True
