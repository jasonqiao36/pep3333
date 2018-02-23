HELLO_WORLD = b'Hello World! by jason\n'


def simple_app(environ, start_response):
    """
    扮演应用端角色，类似Flask。
    提供状态码和头部信息，返回响应字符串。
    服务端收到客户端HTTP请求后，将调用simple_app。
    """
    status = '200 OK'
    resp_headers = [('Content-Type', 'text/plain')]
    start_response(status, resp_headers)
    return [HELLO_WORLD]


class AppClass:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        status = '200 OK'
        resp_headers = [('Content-Type', 'text/plain')]
        self.start(status, resp_headers)
        yield HELLO_WORLD
