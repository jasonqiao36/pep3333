from wsgiref.simple_server import make_server


if __name__ == '__main__':
    from app_side import simple_app

    httpd = make_server('', 8000, simple_app)
    httpd.serve_forever()
