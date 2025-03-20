from threading import Thread

from cheroot.wsgi import Server


class CherootServer:
    def __init__(self, app, args):
        self._thread = None
        self._server = Server(
            wsgi_app=app,
            bind_addr=(args['ip'], args['port']),
        )
        
    def start(self):
        self._server.prepare()
        self._thread = Thread(target=self._server.serve)
        self._thread.start()
        
        return self

    def stop(self):
        self._server.stop()
