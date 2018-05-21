"""
利用socket实现Web服务器
python3
"""
# coding=utf8

import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = b"Hello World! <h1>%s Jason</h1>" % '你好'.encode('utf8')
resp_params = [
    b'HTTP/1.0 200 OK',
    b'Date: Sat, 10 jun 2017 01:01:01 GMT',
    b'Content-Type:text/html;charset=utf-8',
    b'Content-Length:%d\r\n' % len(body),
    body,
]
resp = b'\r\n'.join(resp_params)


def handle_connection(conn, addr):
    request = b''
    # 请求完成标志位
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)

    conn.send(resp)
    conn.close()


def main():
    # socket.AF_INET    用于服务器之间网络通信
    # socket.SOCK_STREAM    基于TCP的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证我们每次Ctrl C之后，快速再次重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8080))
    # 设置连接数
    serversocket.listen(1)
    print('http://127.0.0.1:8080')

    try:
        while True:
            conn, addr = serversocket.accept()
            handle_connection(conn, addr)
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
