import SimpleHTTPServer
import SocketServer

class Server:

	def __init__(self, port):
		self.port = port

	def start(self):
		try:
			handler = SimpleHTTPServer.SimpleHTTPRequestHandler
			httpd = SocketServer.TCPServer(('', self.port), handler)
			print 'Starting server at port {0}'.format(self.port)
			httpd.serve_forever()
		except Exception as e:
			print e

