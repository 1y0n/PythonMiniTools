#coding:utf-8

#Based on code from <Black Hat Python>

import socket
import optparse
import sys
import threading
import subprocess

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while True:
            recv_len = 1
            response = ''
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print response
            buffer = raw_input("")
            buffer += '\n'
            client.send(buffer)
    except:
        print '[*] Error!'
        client.close()

def server_loop():
    global target
    if not len(target):
        target = '127.0.0.1'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command.\n'
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    if len(upload_dest):
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        try:
            file = open(upload_dest, 'wb')
            file.write(file_buffer)
            file.close()
            client_socket.send('Successfully saved file to %s\n' % upload_dest)
        except:
            client_socket.send('Failed to save file to %s\n' % upload_dest)
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)
    if command:
        while True:
            client_socket.send('<#>')
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                response = run_command(cmd_buffer)
                client_socket.send(response)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-l', '--listen', dest='listen', action='store_true', default=False)
    parser.add_option('-e', '--execute', dest='execute', default='')
    parser.add_option('-c', '--commandshell', dest='commandshell', action='store_true', default=False)
    parser.add_option('-u', '--upload', dest='upload', default='')
    parser.add_option('-t', '--target', dest='target', default='')
    parser.add_option('-p', '--port', dest='port', type='int', default=0)
    (options, args) = parser.parse_args()
    execute = options.execute
    command = options.commandshell
    target = options.target
    port = options.port
    upload_dest = options.upload
    if not options.listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
    if options.listen:
        server_loop()
