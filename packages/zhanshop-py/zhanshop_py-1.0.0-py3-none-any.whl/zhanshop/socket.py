import socket as std_socket

class Socket():
    AF_INET = std_socket.AF_INET
    AF_INET6 = std_socket.AF_INET6
    #AF_UNIX = std_socket.AF_UNIX

    SOCK_STREAM = std_socket.SOCK_STREAM
    SOCK_DGRAM = std_socket.SOCK_DGRAM
    SOCK_RAW = std_socket.SOCK_RAW
    SOCK_RDM = std_socket.SOCK_RDM

    MSG_WAITALL = std_socket.MSG_WAITALL
    MSG_PEEK = std_socket.MSG_PEEK
    MSG_OOB = std_socket.MSG_OOB

    socket = None
    errCode = 0
    def __init__(self, family, type, proto = 0, fileno = None):
        """
        @param family: 地址家族 【AF_INET: IPv4地址, AF_INET6: IPv6地址, AF_UNIX: 本地套接字（仅限UNIX系统）】
        @param type: 套接字类型 【SOCK_STREAM: TCP套接字, SOCK_DGRAM: UDP套接字, SOCK_RAW: 原始套接字，通常用于底层网络操作, SOCK_SEQPACKET: 面向连接的不可变长度的数据报套接字】
        @param proto: 协议号【通常设置为0，表示使用默认协议。对于TCP和UDP，通常无需更改】
        @param fileno: 文件描述符，通常不需要设置，除非你有特定的需求
        """
        self.socket = std_socket.socket(family, type, proto, fileno)
        self.errCode = 0

    def setblocking(self, flag):
        """
        @param flag: True表示阻塞模式，False表示非阻塞模式
        @return:
        """
        return self.socket.setblocking(flag) # flag=False 为非阻塞模式
    def connect(self, host, port, timeout = 5):
        """
        连接到远程服务器
        @param host:
        @param port:
        @param timeout:
        @return:
        """
        self.socket.settimeout(timeout)
        status = -3
        try:
            # 尝试连接到服务器
            self.socket.connect((host, port))
            self.errCode = 0
            return True
        except std_socket.timeout:
            self.errCode = -1
            return False
        except Exception:
            self.errCode = -2

        return False

    def send(self, message):
        """
        发送消息
        @param message:
        @return:
        """
        if type(message) != bytes:
            message = message.encode('utf-8')
        print("数据发送了")
        self.socket.sendall(message)
        print("数据发送了")

    def recv(self, buflen = 1024, flags = 0):
        """
        接收消息
        @param buflen: 指定接收缓冲区的大小（以字节为单位）
        @param flags: 指定一些操作标志【MSG_WAITALL: 等待直到接收到完整的缓冲区大小的数据量，MSG_PEEK: 接收数据但不从套接字缓冲区中删除这些数据，MSG_DONTWAIT (在某些系统上可用): 使操作非阻塞，MSG_OOB: 接收或发送带外数据】
        @return:
        """
        try:
            data = self.socket.recv(buflen, flags)
            if not data:
                return b""
            elif(len(data) > 0):
                return data
            return False
        except std_socket.timeout:
            return False
        except Exception as e:
            return b""



    def close(self):
        """
        关闭连接
        @return:
        """
        return self.socket.close()

    @staticmethod
    def gethostbyname(hostname):
        """
        域名解析
        :return:
        """
        addrInfo = []
        addr_info = std_socket.getaddrinfo(hostname, None)  # None 表示不指定端口号
        for family, socktype, proto, canonname, sockaddr in addr_info:
            addrInfo = [family, sockaddr[0]]
            break
        return addrInfo

    def fd(self):
        """
        获取文件描述符
        @return:
        """
        return self.socket.fileno()