import os, sys

# surrogateescape 是一种可逆的错误处理机制，利用 Surrogate 码位保存无法解码的字节，编码时则将其还原为对应的原始字节。
enc, esc = sys.getfilesystemencoding(), 'surrogateescape'


def unicode_to_wsgi(u):
    # Convert an environment variable to a WSGI "bytes-as-unicode" string
    # iso-8859-1就是latin-1
    return u.encode(enc, esc).decode('iso-8859-1')


def wsgi_to_bytes(s):
    # 处理头部信息，转化为native string
    return s.encode('iso-8859-1')


def run_with_cgi(application):
    """
    1. 服务端收到HTTP请求后，生成environ字典，传递给可调用的application
   （这个例子中，就是run_simpl:e)。
    2. start_response生成响应头。还要作为参数传递给application
    write(data)调用write方法，写入响应body
    """

    # os.environ    获取操作系统定义的环境变量
    environ = {k: unicode_to_wsgi(v) for k, v in os.environ.items()}
    environ['wsgi.input'] = sys.stdin.buffer    # sys.stdin 用于交互式输入
    environ['wsgi.errors'] = sys.stderr         # sys.stderr 用于错误信息
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        out = sys.stdout.buffer
        if not headers_set:
            raise AssertionError('write() before start_response()')

        elif not headers_sent:
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes('Status: %s\r\n' % status))
            for header in response_headers:
                out.write(wsgi_to_bytes('%s: %s\r\n' % header))
            out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None
        elif headers_set:
            raise AssertionError('Headers already set!')

        headers_set[:] = [status, response_headers]

        # Note: error checking on the headers should happen here

        return write
    print('1')
    result = application(environ, start_response)
    print(result)
    print('2')
    try:
        for data in result:
            print('3')
            if data:
                write(data)     # don't send headers until body appears
        if not headers_sent:
            write('')       # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()


if __name__ == '__main__':
    from app_side import simple_app

    run_with_cgi(simple_app)
