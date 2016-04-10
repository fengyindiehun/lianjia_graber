# coding:utf-8
#import BeautifulSoup
#import BeautifulSoup
import urllib
import urllib2
import sys
from bs4 import BeautifulSoup

while True:
    print 'aaa'

fd = open('b.html', 'r')
jsessionid = fd.read()
soup = BeautifulSoup(jsessionid)
print soup.find(id='post_user_input').get('value')
print soup.find(id='post_uid_input').get('value')
print soup.find(name='input', attrs={'name':'marketemail'}).get('value')
print soup.find(id='post_phone_input').get('value')

def get_jsessionid_from_file():
    fd = open('jsessionid.txt', 'r')
    jsessionid = fd.readline()
    fd.close()
    return jsessionid

def dongchengjiaoshui_addtocart(jsessionid):
    url = 'http://bjxwgl.homelink.com.cn/product/product_addTSProductToCart.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    svpdId = '2925'
    buyNum = '1'
    colorId = '2188'
    sizeId = '2566'
    form_data = {'svpdId' : svpdId, 'buyNum' : buyNum, 'colorId' : colorId, 'sizeId' : sizeId}
    data_encoded = urllib.urlencode(form_data)
    fd_read = opener.open(url, data_encoded)
    html_content = fd_read.read()
    return html_content

def get_user_pay_account_list():
    #jsessionid = '1EBA3DE110DA020099C7E25B8A5BC356'
    jsessionid = get_jsessionid_from_file()
    #jsessionid = '3A03AEAC16E8D9770975C229B79241EC'
    url = 'http://bjxwgl.homelink.com.cn/order/order_getUserPayAccountList.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    opener.addheaders.append(('Origin', 'http://bjxwgl.homelink.com.cn'))
    opener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
    opener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6'))
    opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'))
    opener.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded'))
    opener.addheaders.append(('Accept', 'text/html, */*'))
    opener.addheaders.append(('Cache-Control', 'max-age=0'))
    opener.addheaders.append(('X-Requested-With', 'XMLHttpRequest'))
    opener.addheaders.append(('Connection', 'keep-alive'))
    opener.addheaders.append(('Referer', 'http://bjxwgl.homelink.com.cn/product/product_toOrderTSApply.action'))
    #form_data = post_info_map
    spvdCode = 'ZN0870,'
    svpdDetailCategory = '101336,'
    form_data = {'spvdCode':spvdCode, 'svpdDetailCategory':svpdDetailCategory}
    data_encoded = urllib.urlencode(form_data)
    fd_read = opener.open(url, data_encoded)
    html_content = fd_read.read()
    print html_content
    #soup = BeautifulSoup(html_content)
    ##print soup.find(id='post_user_input').get('value')
    #a = soup.find_all(name='input', attrs={'name':'post_account'})
    #for i in a:
    #    print i.get('value')

#jsessionid = get_jsessionid_from_file()
#dongchengjiaoshui_addtocart(jsessionid)
get_user_pay_account_list()
