HELLO_WORLD = b'Hello World! by jason\n'


# 1.可调用对象是一个函数
def simple_app(environ, start_response):
    """扮演应用端角色
    提供状态码和头部信息，返回响应字符串。
    服务端收到客户端HTTP请求后，将调用simple_app。
    """
    status = '200 OK'
    resp_headers = [('Content-Type', 'text/plain')]
    start_response(status, resp_headers)
    return [HELLO_WORLD]


# 2.可调用对象是一个类
class AppClassIter:
    """可调用对象就是AppClass这个类
    调用它可以返回可迭代对象
    使用方法类似于：
    for result in AppClass(environ, start_response):
        do_something(result)
    """
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        status = '200 OK'
        resp_headers = [('Content-Type', 'text/plain')]
        self.start_response(status, resp_headers)
        yield HELLO_WORLD


# 3.可调用对象是一个实例
class AppClass:
    """这里可调用对象是一个实例
    app = AppClassNew()
    for result in app(environ, start_response):
        do_something(result)
    """

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        status = '200 OK'
        resp_headers = [('Content-Type', 'text/plain')]
        start_response(status, resp_headers)
        yield HELLO_WORLD


app = AppClass()
