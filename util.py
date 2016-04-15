# coding:utf-8

import urllib
import urllib2
from bs4 import BeautifulSoup
import sys
import datetime

def get_jsessionid_from_file():
    fd = open('jsessionid.txt', 'r')
    jsessionid = fd.readline()
    fd.close()
    return jsessionid

def write_jsessionid_to_file(jsessionid):
    fd = open('jsessionid.txt', 'w')
    fd.write(jsessionid)
    fd.close()

def get_jsessionid():
    url = 'http://bjxwgl.homelink.com.cn/'
    header = urllib.urlopen(url).info()
    cookie = header['Set-Cookie']
    print 'The value of Set-Cookie is:' + cookie
    semicolon_pos = cookie.find(';')
    equal_pos = cookie.find('=')
    jsessionid = cookie[equal_pos+1 : semicolon_pos]
    print 'The value of jsessionid is:' + jsessionid
    write_jsessionid_to_file(jsessionid)

def get_captcha():
    jsessionid = get_jsessionid_from_file()
    url = 'http://bjxwgl.homelink.com.cn/usr/loginCaptcha.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    fd_read = opener.open(url)
    captcha_content = fd_read.read()
    fd_write = open('./static/captcha.jpg', 'w')
    fd_write.write(captcha_content)
    fd_write.close()

def user_login(username, password, captcha):
    jsessionid = get_jsessionid_from_file()
    url = 'http://bjxwgl.homelink.com.cn/usr/login.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    opener.addheaders.append(('Origin', 'http://bjxwgl.homelink.com.cn'))
    opener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
    opener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6'))
    opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'))
    opener.addheaders.append(('HTTPS', '1'))
    opener.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded'))
    opener.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'))
    opener.addheaders.append(('Cache-Control', 'max-age=0'))
    opener.addheaders.append(('Referer', 'http://bjxwgl.homelink.com.cn/'))
    opener.addheaders.append(('Connection', 'keep-alive'))
    form_data = {'userCode' : username, 'password' : password, 'captcha' : captcha, 'urlcode' : '/'}
    data_encoded = urllib.urlencode(form_data)
    print data_encoded
    fd_read = opener.open(url, data_encoded)
    print 'hh'
    print fd_read.getcode()
    print fd_read.info()
    html_content = fd_read.read()
    print html_content

def monica():
    if str(datetime.datetime.now()) > '2016-04-23':
        sys.exit()
