#coding:utf-8

import logging
#get rid of the Warning
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import Queue
from threading import Thread
import optparse

def tcp_connect_scan(dst_ip, src_port):
	while not Port_Queue.empty():
		dst_port = Port_Queue.get()
		resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='S'), timeout=10)
		if (str(type(resp)) == "Type <None Type>"):
			print '[*] %d    Closed.' % dst_port
		elif (resp.haslayer(TCP)):
			if (resp.getlayer(TCP).flags == 0x12):
				send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='AR'), timeout=10)
				print '[*] %d     Open.' % dst_port
			elif (resp.getlayer(TCP).flags == 0x14):
				print '[*] %d    Closed.' % dst_port

def tcp_syn_scan(dst_ip, src_port):
	while not Port_Queue.empty():
                dst_port = Port_Queue.get()
                resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='S'), timeout=10)
                if (str(type(resp)) == "Type <None Type>"):
                        print '[*] %d    Filtered.' % dst_port
                elif (resp.haslayer(TCP)):
                        if (resp.getlayer(TCP).flags == 0x12):
                                send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='R'), timeout=10)
                                print '[*] %d     Open.' % dst_port
                        elif (resp.getlayer(TCP).flags == 0x14):
                                print '[*] %d    Closed.' % dst_port
		elif (resp.haslayer(ICMP)):
			if (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
				print '[*] %d    Filtered.' % dst_port

def tcp_ack_scan(dst_ip):
        while not Port_Queue.empty():
                dst_port = Port_Queue.get()
                resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port, flags='A'), timeout=10)
                if (str(type(resp)) == "Type <None Type>"):
                        print '[*] %d    Filtered.' % dst_port
                elif (resp.haslayer(TCP)):
                        if (resp.getlayer(TCP).flags == 0x4):
                                print '[*] %d     Unfiltered.' % dst_port
                elif (resp.haslayer(ICMP)):
                        if (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                                print '[*] %d    Filtered.' % dst_port


if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-i', '--ip', dest='target_ip')
	parser.add_option('-o', '--port', dest='target_port', default='1-65535')
	parser.add_option('-m', '--method', dest='method', default='cnt', help='cnt/syn/ack')
	parser.add_option('-t', '--thread', dest='threads', type='int', default=1)
	(options, args) = parser.parse_args()
	Port_Queue = Queue.Queue()
	thread_list = []
	cmd_dir = {'cnt': 'Thread(target=tcp_connect_scan(options.target_ip, RandShort()))',
		   'syn': 'Thread(target=tcp_syn_scan(options.target_ip, RandShort()))',
	           'ack': 'Thread(target=tcp_ack_scan(options.target_ip))'
		  }
	if (options.target_ip == ''):
		print '[!] Need a target IP!'
		exit(0)
	else:
		port_list = options.target_port.split(',')
		for port in port_list:
			if '-' in port:
				tmp_port_list = port.split('-')
				for i in range(int(tmp_port_list[0]), int(tmp_port_list[-1]) + 1):
					Port_Queue.put(int(i))
			else:
				Port_Queue.put(int(port))
	string = 'Thread(target=tcp_connect_scan(options.target_ip, RandShort()))'
 	if options.method in ['cnt', 'syn', 'ack']:
		for i in range(options.threads):
			t = eval(cmd_dir[options.method])
			thread_list.append(t)
			t.start()
		for t in thread_list:
			t.join()
	else:
		print '[!] Not support this method!'
		exit(0)
