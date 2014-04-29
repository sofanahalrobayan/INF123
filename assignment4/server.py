from network import Listener, Handler, poll
 
handlers = {}  # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
    	pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        print msg
	
	def  _accept_connection(port):
   		listen_socket = socket.socket()
   		listen_socket.bind(('', port))
    	print('\nWaiting for a connection from a client...')
    	listen_socket.listen(0)
    	connect_socket, from_address = listen_socket.accept()
    	listen_socket.close()
    	return _build_connection_object(connect_socket)
 
 
port = 8888
server = Listener(port, MyHandler)

while 1:
    poll(timeout=0.05) # in seconds
    server.on_open()
