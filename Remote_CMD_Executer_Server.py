#coding:utf-8

import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('127.0.0.1', 10000))
server.listen(5)
print '[*] Listening on 127.0.0.1:10000'


def handle_client(client_socket):
	while True:
		try:
			result = client_socket.recv(2048)
			print '[*] Recv: %s' % result
			cmd = raw_input('-----input cmd-----\n')
			client_socket.send(cmd)
		except  KeyboardInterrupt:
			exit()

while True:
	try:
		client, (ip, port) = server.accept()
		print '[*] Accepted connection from: %s:%d' % (ip, port)
		client_handler = threading.Thread(target=handle_client, args=(client, ))
		client_handler.start()
	except KeyboardInterrupt:
		exit()
