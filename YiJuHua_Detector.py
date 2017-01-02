#coding:utf-8

import re
import threading
import os
import Queue
import urllib2

__author__ = '1y0n'

#网站URL
base_url = 'http://localhost/'
#网站根目录
root_dir = 'D:\\phpStudy\\WWW'
#危险函数
danger_fuc_list = ['eval', 'assert', 'preg_replace']
#是否启用动态检测
allow_dynamic_detect = False
file_q = Queue.Queue()
d_file_q = Queue.Queue()


def str_rot13(text):
    return text.decode("rot13")


def base64_decode(text):
    return text.decode("base64")


def str_replace(ptn, repl, text):
    return text.replace(ptn, repl)


def decoder(text): #解码PHP代码，目前支持str_rot13,base64解码和str_replace字符(串)替换
    r1 = ''
    r2 = ''
    r3 = ''
    if 'base64_decode' in text:
        result = re.findall('base64_decode\(.*?\)', text, re.I)
        for i in result:
            try:
                num = len(re.findall('\(', i)) - len(re.findall('\)', i))
                i += ')' * num
                r1 = eval(i)
            except:
                pass
    if 'str_rot13' in text:
        result = re.findall('str_rot13\(.*?\)', text, re.I)
        for i in result:
            try:
                num = len(re.findall('\(', i)) - len(re.findall('\)', i))
                i += ')' * num
                r2 = eval(i)
            except:
                pass
    if 'str_replace' in text:
        result = re.findall('str_replace\(.*?\)', text, re.I)
        for i in result:
            try:
                num = len(re.findall('\(', i)) - len(re.findall('\)', i))
                i += ')' * num
                r3 = eval(i)
            except:
                pass
    if r1 in danger_fuc_list or r2 in danger_fuc_list or r3 in danger_fuc_list:
        return True #存在经过编码的危险函数说明代码有问题
    else:
        return False


def array_map_detect(text):
    array_map_pattern_1 = re.compile(r'array_map\(.*?\$_(POST|REQUEST)', re.I)
    array_map_pattern_2 = re.compile(r'array_map\(.*?(\$\w+?)', re.I)
    if re.findall(array_map_pattern_1, text):
        return True
    result_list = re.findall(array_map_pattern_2, text)
    if result_list:
        for result in result_list:
            if re.findall('\\'+result+'\s*?=\s*?\$_(POST|REQUEST)', text, re.I):
                return True
    pass

def static_detect():#静态检测
    filename = file_q.get()
    with open(filename) as f:
        text = f.read()
    if decoder(text):
        print u'[!] %s      经过编码的危险函数' % filename
    if array_map_detect(text):
        print u'[!] %s      array_map型一句话' % filename
    preg_re_pattern = re.compile(r'preg_replace(.*?)/e(.*?)\$', re.I)
    eval_pattern = re.compile(r'eval\(.*?\$.*?\)', re.I)
    assert_pattern = re.compile(r'assert\(.*?\$.*?\)', re.I)
    preg_re_pattern_1 = re.compile(r'p.*?r.*?e.*?g.*?_.*?r.*?e.*?p.*?l.*?a.*?c.*?e.*?\\e', re.I)
    eval_pattern_1 = re.compile(r'e.*?v.*?a.*?l', re.I)
    assert_pattern_1 = re.compile(r'a.*?s.*?s.*?e.*?r.*?t', re.I)
    array_map_pattern_1 = re.compile(r'a.*?r.*?r.*?a.*?y.*?_.*?m.*?a.*?p', re.I)
    extra_pattern_1 = re.compile(r'(\$\w+?)\(\$', re.I)
    danger_var_list = re.findall(extra_pattern_1, text)
    r1 = re.findall(preg_re_pattern,text)
    r2 = re.findall(eval_pattern, text)
    r3 = re.findall(assert_pattern, text)
    if r1 or r2 or r3:
        print u'[!] %s      危险函数内发现变量  %s - %s - %s' % (filename, r1, r2, r3)
    if danger_var_list:
        for danger_var in danger_var_list:
            result = ''.join(re.findall('\\' + danger_var + '.*?=.*?\w*?;', text, re.I))
            if re.findall(preg_re_pattern_1, result) or re.findall(eval_pattern_1, result) or re.findall(assert_pattern_1, result)\
                    or re.findall(array_map_pattern_1, result):
                print u'[!] %s      可疑的变量 %s ，拼接了危险函数 %s' % (filename, danger_var, result)


def dynamic_detect():#动态检测
    filename = d_file_q.get()
    post_pattern = re.compile(r'\$_(POST|REQUEST)(\[|\[\'|\[\")(\w*?)(\]|\'\]|\"\])', re.I)
    f = open(filename, 'r')
    var_list = re.findall(post_pattern, f.read())
    f.close()
    url = filename.replace(root_dir, base_url)
    url = url.replace('\\', '/')
    for var in var_list:
        data = '%s=@eval(base64_decode($_POST[z0]));&z0=ZWNobygieWlqdWh1YWRldGVjdCIpO2RpZSgpOw==' % var[2]
        result = urllib2.urlopen(url, data=data).read()
        if re.findall(r"yijuhuadetect", result, re.I):
            print u'[!] %s     疑似一句话(动态检测)' % filename
        else:
            print u'[!] %s     动态检测未检出' % filename


def get_all_file(dir, filelist): #爬行给定目录下所有文件
    newDir = dir
    if os.path.isfile(dir):
        filelist.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_all_file(newDir, filelist)
    return filelist


def start_detect(dir):
    t_list = []
    for f in get_all_file(dir, []):
        if f.endswith('.php'):
            file_q.put(f)
            d_file_q.put(f)
    print u'[*] 获取到 %d 个文件。开始检测...' % file_q.qsize()
    for i in range(file_q.qsize()):
        t = threading.Thread(target=static_detect())
        t_list.append(t)
        t.start()
    for tt in t_list:
        tt.join()
    if allow_dynamic_detect:
        print u'[*] 开始动态检测...'
        for i in range(d_file_q.qsize()):
            dt = threading.Thread(target=dynamic_detect())
            t_list.append(dt)
            dt.start()
        for dt in t_list:
            dt.join()

if __name__ == '__main__':
    print u'[*] 爬行指定文件...'
    start_detect('D:\\phpStudy\\WWW\\evaltest') #要扫描的目录
    print u'[*] 完成！'
