from gevent.pywsgi import WSGIServer
from flaskr import create_app


if __name__ == '__main__':
    app = create_app()
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
