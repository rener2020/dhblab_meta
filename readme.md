# 通讯流程
![](./doc/通讯流程图.png)


# 服务端配置运行

1. 配置主机$IP$地址与端口 \
  在`./module/server/server.py`第`123`行配置
3. 在项目目录打开命令行，运行服务端 \
  `python server_start.py`
# 客户端配置运行
1. 配置服务端$IP$地址与端口 \
在`./module/client/client.py`第`57`行配置
2. 配置客户端名称 \
在`./module/client/client.py`第`23`行配置
3. 在项目目录打开命令行，运行服务端 \
  `python client_start.py`

# 如何使用
本项目的目的是让用户在忘记通讯的时候实现通讯，将复杂的通讯流程简化为简单的文件读取操作，用户不需要关心通讯过程的具体实现
## 向其他客户端发送数据
向`./send_cache.txt`文件中写入需要发送的数据内容
## 同步其他客户端发送的数据
从`./recv_cache.txt`文件中读取数据内容