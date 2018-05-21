class Upperware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        for data in self.application(environ, start_response):
            yield data.upper()


if __name__ == '__main__':
    from app_side import simple_app
    from server_side import run_with_cgi

    application = Upperware(simple_app)
    run_with_cgi(application)
