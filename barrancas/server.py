import http.server
import socketserver


class Server:

    def __init__(self, port, directory):
        self.port = port
        self.directory = directory


    @classmethod
    def handler_from(cls, directory):
        def _init(self, *args, **kwargs):
            return http.server.SimpleHTTPRequestHandler.__init__(
                self, *args, directory=self.directory, **kwargs
            )

        return type(
            f"HandlerFrom<{directory}>",
            (http.server.SimpleHTTPRequestHandler,),
            {"__init__": _init, "directory": directory},
    )

    def start(self):
        try:
            handler = Server.handler_from(self.directory)
            httpd = socketserver.TCPServer(("", self.port), handler)
            print(f"Starting server at port {self.port}")
            httpd.serve_forever()
        except Exception as e:
            print(e)
