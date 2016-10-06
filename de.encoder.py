#coding:utf-8

import binascii
import sys
from hashlib import md5
from urllib import quote, unquote
from selenium import webdriver  #mechanize is a better choice. i dont test POST ;)
import re

class decoder():
    def __init__(self, code):
        self.code = code
        self.decode_list = {'Base64': "binascii.a2b_base64(self.code + '=' * int(len(self.code) % 4))",
                            'HEX': "binascii.a2b_hex(self.code)",
                            'URL': "unquote(self.code)",
                            'Chr': 'chr(int(self.code))',
                            'Ord': 'ord(self.code)'}

    def decode(self):
        print '-----------Decode Result Of %s-----------' % self.code
        for item, value in self.decode_list.items():
            try:
                print '%s: %s' % (item, eval(value))
            except:
                print '[!] Failed to decode as %s' % item
        self.md5_decode()

    def md5_decode(self):
        print '[*] It will take sometime to get MD5,please wait...'
        try:
            driver = webdriver.PhantomJS('phantomjs.exe') #Require phantomjs!
            #driver = webdriver.Firefox()                 or use this
            driver.get('http://www.cmd5.com/')
            input = driver.find_element_by_name('ctl00$ContentPlaceHolder1$TextBoxInput')
            submit = driver.find_element_by_name('ctl00$ContentPlaceHolder1$Button1')
            input.send_keys(self.code)
            submit.click()
            print 'MD5: ', re.findall('<span id="ctl00_ContentPlaceHolder1_LabelAnswer">(.*?)[<br>|<a]', driver.page_source, re.I)[0]
        except:
            print '[!] Failed to decode as MD5'
        finally:
            driver.close()


class encoder():
    def __init__(self, code):
        self.code = code
        self.encode_list = {'Base64': "binascii.b2a_base64(self.code)",
                            'HEX': "binascii.b2a_hex(self.code)",
                            'URL(GBK)': "quote(self.code.decode(sys.stdin.encoding).encode('gbk'))",
                            'URL(UTF-8)': "quote(self.code.decode(sys.stdin.encoding).encode('utf-8'))",
                            'Chr': 'chr(int(self.code))',
                            'Ord': 'ord(self.code)'}

    def encode(self):
        print '-----------Encode Result Of %s-----------' % self.code
        for item, value in self.encode_list.items():
            try:
                print '%s: %s' % (item, eval(value))
            except:
                print '[!] Failed to encode as %s' % item
        self.md5_encode()

    def md5_encode(self):
        try:
            md = md5()
            md.update(self.code)
            print 'MD5: ', md.hexdigest()
        except:
            print '[!] Failed to encode as MD5'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print
        '''Usage:
                Encode: python de.encoder.py StringToEncode -e
                Decode: python de.encoder.py StringToDecode'''
    elif sys.argv[2] == '-e':
        encode = encoder(sys.argv[1])
        encode.encode()
    else:
        decode = decoder(sys.argv[1])
        decode.decode()