# coding:utf-8

import urllib
import urllib2
from bs4 import BeautifulSoup
import sys

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
    form_data = {'userCode' : username, 'password' : password, 'captcha' : captcha, 'urlcode' : '/'}
    data_encoded = urllib.urlencode(form_data)
    fd_read = opener.open(url, data_encoded)
