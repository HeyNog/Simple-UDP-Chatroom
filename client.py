import socket
import tkinter as tk
from tkinter import messagebox
import threading
import time
import sys

global s, online_flag, my_addr
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
online_flag = False
my_addr = 'Unknown'

def message_decode(byte_data, codetype='utf-8'):
	return byte_data.decode(codetype)

def message_encode(message, codetype='utf-8'):
	return message.encode(codetype)

main_window = tk.Tk(className='UDP_Chatter')
address = tk.Variable()
address.set('127.0.0.1')
port = tk.IntVar()
port.set(9999)
message = tk.Variable()
user_name = tk.Variable()

def message_wrap(message, codetype='utf-8'):
	global my_addr
	_user_name = user_name.get()
	if _user_name == '':
		_user_name = 'Anonymous'
	sendfrom = '%s (%s)'%(_user_name, my_addr)
	message = '\n%s\n%s'%(sendfrom, message)
	return message.encode(codetype)

printer = tk.Text(main_window)
scroll = tk.Scrollbar()

scroll.config(command=printer.yview)
printer.config(yscrollcommand=scroll.set, state=tk.DISABLED)

def _print(print_obj, tktext_obj=printer):
	tktext_obj.config(state=tk.NORMAL)
	tktext_obj.insert(tk.END, str(print_obj)+'\n')
	tktext_obj.config(state=tk.DISABLED)
	print(print_obj)

def send_message():
	global s, online_flag
	print(online_flag)
	_address = address.get()
	_port = port.get()
	addr = (_address, _port)
	_message = message.get()
	s.sendto(message_wrap(_message), addr)
	message.set('')

def send_on_click(event):
	send_message()

address_entry = tk.Entry(main_window, textvariable=address)
port_entry = tk.Entry(main_window, textvariable=port)
message_entry = tk.Entry(main_window, textvariable=message)
ip_label = tk.Label(main_window, text='Chat Room Server IP : Port')
send_button = tk.Button(main_window, text='Send', command=send_message)
main_window.bind('<Return>', send_on_click)
user_label = tk.Label(main_window, text='User Name :')
user_entry = tk.Entry(main_window, textvariable=user_name)

send_button.config(state=tk.DISABLED)

def log_in_fun():
	global online_flag, my_addr
	_address = address.get()
	_port = port.get()
	addr = (_address, _port)
	if not(online_flag):
		s.sendto(message_wrap('Coming in...'), addr)
		_print('Connecting to Chatroom Server...')
		_print(s.recv(1024).decode('utf-8'))
		my_addr = message_decode(s.recv(1024))
		online_flag = True
		address_entry.config(state=tk.DISABLED)
		port_entry.config(state=tk.DISABLED)
		user_entry.config(state=tk.DISABLED)
		send_button.config(state=tk.NORMAL)

def log_out_fun():
	global online_flag
	_address = address.get()
	_port = port.get()
	addr = (_address, _port)
	if online_flag:
		s.sendto(message_encode('exit'), addr)
		online_flag = False
		address_entry.config(state=tk.NORMAL)
		port_entry.config(state=tk.NORMAL)
		user_entry.config(state=tk.NORMAL)
		send_button.config(state=tk.DISABLED)

def on_closing():
	global online_flag
	online_flag = True
	if messagebox.askokcancel("UDP_Chatter", "Do you want to quit and logout?"):
		log_out_fun()
		main_window.destroy()
		sys.exit()

login_button = tk.Button(main_window, text='Login', command=log_in_fun)
logout_button = tk.Button(main_window, text='Logout', command=log_out_fun)

login_button.grid(row=1, column=4, sticky='ew')
logout_button.grid(row=2, column=4, sticky='ew')
ip_label.grid(row=1, column=1, sticky='w')
address_entry.grid(row=1, column=2, sticky='ew')
port_entry.grid(row=1, column=3, sticky='ew')
user_label.grid(row=2, column=1, sticky='w')
user_entry.grid(row=2, column=2, columnspan=2, sticky='ew')
printer.grid(row=3, rowspan=10, column=1, columnspan=4, sticky='ew')
scroll.grid(row=3, rowspan=10, column=5, sticky='e')
message_entry.grid(row=13, column=1, columnspan=3, sticky='ew')
send_button.grid(row=13, column=4, sticky='ew')

def receive():
	global online_flag, s
	while True:
		time.sleep(0.1)
		if online_flag:
			receive_message = s.recv(1024)
			receive_message = message_decode(receive_message)
			_print(receive_message)

if __name__ == '__main__':
	main_window.protocol("WM_DELETE_WINDOW", on_closing)
	t = threading.Thread(target=receive)
	t.start()
	main_window.mainloop()
	
# # 建立连接:
# s.connect(('127.0.0.1', 9999))
# # 接收欢迎消息:
# print(s.recv(1024).decode('utf-8'))
# for data in [b'Michael', b'Tracy', b'Sarah']:
# 	# 发送数据:
# 	s.send(data)
# 	print(s.recv(1024).decode('utf-8'))
# s.send(b'exit')
# s.close()
