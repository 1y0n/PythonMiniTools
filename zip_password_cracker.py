#coding:utf-8

import zipfile
import optparse
import Queue
from threading import Thread
import time

def zip_cracker(zFile):
    while not queue.empty():
        try:
            password = queue.get()
            zFile.extractall(pwd=password)
            print '******PASSWORD FOUND!******\nPassword: %s' % password
        except:
            pass

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    parser.add_option('-t', dest='threads', type='int', default=2)
    (options, args) = parser.parse_args()
    if ((options.zname == None) | (options.dname == None)):
        print 'USAGE:\n       zip_cracker.py -f [filename] -d [Dictionary]'
        exit(-1)
    else:
        print '[*] Starting crack %s with thread %d' % (options.zname, options.threads)
        queue = Queue.Queue()
        thread_list = []
        zFile = zipfile.ZipFile(options.zname)
        passfile = open(options.dname)
        start_time = time.time()
        for line in passfile.readlines():
            queue.put(line.rstrip())
        passfile.close()
        for n in range(options.threads):
            t = Thread(target=zip_cracker(zFile))
            t.start()
            thread_list.append(t)
        for i in thread_list:
            i.join()
        print '[*] Finished in %.3f s' % (time.time() - start_time)