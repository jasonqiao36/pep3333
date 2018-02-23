"""
complete a web server by socket
python2
"""
# coding=utf8

import socket

EOL1 = '\n\n'
EOL2 = '\n\r\n'
body = """Hello World! <h1>你好 Jason</h1>"""
resp_params = [
    'HTTP/1.0 200 OK',
    'Date: Sat, 10 jun 2017 01:01:01 GMT',
    'Content-Type:text/html;charset=utf-8',
    'Content-Length:{}\r\n'.format(len(body)),
    body,
]
resp = b'\r\n'.join(resp_params)


def handle_connection(conn, addr):
    request = ''
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
    serversocket.bind(('0.0.0.0', 8080))
    # 设置连接数
    serversocket.listen(1)
    print('http://0.0.0.0:8080')

    try:
        while True:
            conn, addr = serversocket.accept()
            handle_connection(conn, addr)
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
