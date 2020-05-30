import socket
import time


def socket_web(data_json):
	HOST = '172.29.52.94'
	PORT = 7000
	my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	my_socket.bind((HOST,PORY))
	my_socket.listen(5)
	conn,addr = my_socket.accept()
	conn.send(data_json.encode())
	while True:
		time.sleep(0.4)
		rec = conn.recv(1024)
		msg = rec.decode()
		if msg == "end":
			break
	conn.close()

