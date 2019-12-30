import socket
import threading
import time
import sys

if len(sys.argv)>1:
	PORT = int(sys.argv[1])
else:
	PORT = int(input('Input Port No. to use :'))

global user_list, s, messagebox
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# PORT = 9999
s.bind(('127.0.0.1', PORT))

user_list, messagebox = [], []

def message_decode(byte_data, codetype='utf-8'):
	return byte_data.decode(codetype)

def message_encode(message, codetype='utf-8'):
	return message.encode(codetype)

def message_wrap(message, codetype='utf-8'):
	my_addr = 'ChatRoom Host Server'
	_user_name = 'Room Master'
	sendfrom = '%s (%s)'%(_user_name, my_addr)
	message = '\n%s\n%s'%(sendfrom, message)
	return message.encode(codetype)

def udp_receive():
	global user_list, s, messagebox
	print('Receiving message...')
	while True:
		data, addr = s.recvfrom(1024)
		time.sleep(0.1)
		print(message_decode(data))
		print('from %s:%s'%addr)
		messagebox.append([data, addr])

def udp_broadcast():
	global user_list, s, messagebox
	while True:
		if len(messagebox):
			data, addr = messagebox.pop(0)
			message = message_decode(data)
			try:
				user_index = user_list.index(addr)
			except ValueError as e:
				user_list.append(addr)
				s.sendto(message_wrap('Welcome'), addr)
				s.sendto(message_encode('%s:%s'%addr), addr)
				print(user_list)
			if message == 'exit':
				message = 'User %s:%s Disconnected'%addr
				data = message_wrap(message)
				for user in user_list:
					s.sendto(data, user)
					print('Send to %s:%s'%user)
				user_list.pop(user_index)
				print('User %s:%s Disconnected'%addr)
			else:
				for user in user_list:
					s.sendto(data, user)
					print('Send to %s:%s'%user)

if __name__ == '__main__':
	receiver = threading.Thread(target=udp_receive)
	broadcaster = threading.Thread(target=udp_broadcast)
	receiver.start()
	broadcaster.start()