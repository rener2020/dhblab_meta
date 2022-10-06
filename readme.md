# 通讯流程
![](./doc/通讯流程图.png)


# 运行前准备
需求：\
- python3.8

# 服务端配置运行

1. 配置主机$IP$地址与端口 \
  在`config/server.py`中配置
3. 在项目目录打开命令行，运行服务端 \
  `python server_start.py`
# 客户端配置运行
1. 配置服务端$IP$地址与端口 \
  在`config/client.py`中配置
3. 配置客户端名称 \
  在`config/client.py`中配置`name`字段
4. 在项目目录打开命令行，运行服务端 \
  `python client_start.py`

# 如何使用
本项目的目的是让用户在忘记通讯的时候实现通讯，将复杂的通讯流程简化为简单的文件读取操作，用户不需要关心通讯过程的具体实现

## 向其他客户端发送信息
向`storage/devices/self.txt`文件中写入信息
## 接收其他客户端的信息
从`storage/devices/_{}.txt`文件中读取信息，其中`{}`表示的具体信息为其他客户端中配置的**客户端名称**
