#coding:utf-8

import requests
import Queue
import re
import threading
import time
import optparse

class website_dir_scaner():
    def __init__(self, url, thread, status_list):
        self.dir_queue = Queue.Queue()
        self.baseurl = url
        self.threads = thread
        self.status_list = status_list
        self.total_num = 0
        self.find_num = 0
        self.fail_num = 0

    def get_directory(self):
        try:
            directory = open('directory/website_dir.txt')
            for line in directory.readlines():
                self.dir_queue.put(line.rstrip())
            directory.close()
        except:
            print '[!] ERROR:directory missed!'

    def get_robots(self):
        try:
            url = self.baseurl + r'/robots.txt'
            html = requests.get(url).text
            list = re.findall('Disallow: (.*)', html)
            print '[+] Robots.txt found!'
            for i in list:
                print i
                self.dir_queue.put(i)
        except Exception, e:
            print '[!] ERROR:', e

    def brute_dir(self):
        while not self.dir_queue.empty():
            try:
                url = self.baseurl + '/' + self.dir_queue.get()
                rsp = requests.get(url)
                if self.status_list:
                    if str(rsp.status_code) in self.status_list:
                        print '%d             %s' % (rsp.status_code, url)
                        self.find_num += 1
                else:
                    if rsp.status_code != 404:
                        print '%d             %s' % (rsp.status_code, url)
                        self.find_num += 1
            except:
                self.fail_num += 1
                pass

    def start(self):
        print '[*] Initialing'
        self.get_robots()
        self.get_directory()
        self.total_num = self.dir_queue.qsize()
        print '[*] Starting scan!'
        start_time = time.time()
        thread_list = []
        for thread in range(self.threads):
            t = threading.Thread(target=self.brute_dir())
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()
        print '[*] Scan complete in %.3f s' % (time.time() - start_time)
        print '%d/%d Found! %d failed' % (self.find_num, self.total_num, self.fail_num)

parser = optparse.OptionParser()
parser.add_option('-u', '--url', dest='url', help='The URL to brute')
parser.add_option('-t', '--thread', dest='thread', type='int', default=5)
parser.add_option('-s', '--status', dest='status', help='Status code you want')
(options, args) = parser.parse_args()

if __name__ == '__main__':
    bruter = website_dir_scaner(options.url, options.thread, options.status.split(','))
    bruter.start()