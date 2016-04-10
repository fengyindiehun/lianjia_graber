# coding:utf-8

import urllib
import urllib2
import sys
from bs4 import BeautifulSoup
import db

#####################################################################
#GLOBAL VAR FOR USER
#####################################################################
tsname = None
tsuserid = None
marketemail = None
tsphone = None
accounts = []
#####################################################################




#####################################################################
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
    if html_content is '1':
        print 'http://bjxwgl.homelink.com.cn/product/product_addTSProductToCart.action success'
    else:
        print 'http://bjxwgl.homelink.com.cn/product/product_addTSProductToCart.action failed, error_code is:' + html_content

def dongchengjiaoshui_getuserinfo(jsessionid):
    url = 'http://bjxwgl.homelink.com.cn/product/product_toOrderTSApply.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    svpdId = '2925'
    buyNum = '1'
    colorId = '2188'
    sizeId = '2566'
    form_data = {'svpdId' : svpdId, 'buyNum' : buyNum, 'colorId' : colorId, 'sizeId' : sizeId}
    data_encoded = urllib.urlencode(form_data)
    fd_read = opener.open(url)
    html_content = fd_read.read()
    if html_content is None or html_content == '':
        print 'http://bjxwgl.homelink.com.cn/product/product_toOrderTSApply.action failed'
    else:
        print 'http://bjxwgl.homelink.com.cn/product/product_toOrderTSApply.action success'
    return html_content


def dongchengjiaoshui_submitorder(jsessionid, form_data):
    url = 'http://bjxwgl.homelink.com.cn/order/order_payOrderTSByAccount.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    data_encoded = urllib.urlencode(form_data)
    print 'dongchengjiaoshui form_data:' + data_encoded
    fd_read = opener.open(url, data_encoded)
    html_content = fd_read.read()
    if html_content is '1':
        print 'http://bjxwgl.homelink.com.cn/order/order_payOrderTSByAccount.action success, contract sd:' + form_data['wangqianhetong'] + ' success, '
    else:
        error = 'http://bjxwgl.homelink.com.cn/order/order_payOrderTSByAccount.action failed, contract id:' + form_data['wangqianhetong'] + ' failed, '
        error_msg = ''
        if html_content == '2':
            error_msg = 'only can buy one gift'
        elif html_content == '3':
            error_msg = 'please select account'
        elif html_content == '4':
            error_msg = 'account ' + form_data['post_account'] + ' do not have enough money'
        elif html_content == '5':
            error_msg = 'please at least choose one gift'
        elif html_content == '6':
            error_msg = 'region gift can not buy by personal account'
        elif html_content == '7':
            error_msg = 'personal gift can not buy by public account'
        elif html_content == '8':
            error_msg = 'exclusive account can only by exclusive gift'
        elif html_content == '9':
            error_msg = 'market account can only by market gift'
        elif html_content == '10':
            error_msg = 'recrutiment account can only by recrutiment gift'
        elif html_content == '11':
            error_msg = 'do not have enough gift, please choose other time'
        else:
            error_msg = html_content
        print error + error_msg
    return html_content

def get_user_pay_account_list():
    jsessionid = get_jsessionid_from_file()
    url = 'http://bjxwgl.homelink.com.cn/order/order_getUserPayAccountList.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    #form_data = post_info_map
    spvdCode = 'ZN0870,'
    svpdDetailCategory = '101336,'
    form_data = {'spvdCode':spvdCode, 'svpdDetailCategory':svpdDetailCategory}
    data_encoded = urllib.urlencode(form_data)
    fd_read = opener.open(url, data_encoded)
    html_content = fd_read.read()
    #soup = BeautifulSoup(html_content, 'html.parser')
    soup = BeautifulSoup(html_content)
    accounts = []
    for item in soup.find_all(name='input', attrs={'name':'post_account'}):
        accounts.append(item.get('value').encode('utf-8'))
    return accounts

def parse_cart_info(cart_info):
    global tsname
    global tsuserid
    global marketemail
    global tsphone
    global accounts

    soup = BeautifulSoup(cart_info, 'html.parser', from_encoding='latin-1')
    tsname = soup.find(id='post_user_input').get('value').encode('utf-8')
    tsuserid = soup.find(id='post_uid_input').get('value').encode('utf-8')
    marketemail = soup.find(name='input', attrs={'name':'marketemail'}).get('value').encode('utf-8')
    tsphone = soup.find(id='post_phone_input').get('value').encode('utf-8')
    accounts = get_user_pay_account_list()

    print 'tsname:' + tsname
    print 'tsuserid:' + tsuserid
    print 'marketemail:'+ marketemail
    print 'tsphone:' + tsphone
    print accounts

def get_dongchengjiaoshui_post_datas():
    post_map = []
    svpdUpLoadType = '-1'
    spvdName = '东城预约缴税'
    svpdUpLoadTypeDetail = '-1'
    spvdCode = 'ZN0870'
    svpdDetailCategory = '101336'
    checkBoxProduct = '2925_2188_2566'

    #for line in open('dongchengjiaoshui.txt', 'r'):
    for order_info in db.dongchengjiaoshui_select():
        if order_info[6] != '0':
            continue
        wangqianhetong = order_info[0]
        kehuxingming = order_info[1]
        kehushengfenzheng = order_info[2]
        guohuzhuanyuan = order_info[3]
        yuyueshijian = order_info[4]
        dateType = order_info[5]
        eoContent = '网签合同号：' + wangqianhetong + ',客户姓名：' + kehuxingming + ',身份证号：' + kehushengfenzheng + ',过户专员：' + guohuzhuanyuan + ',预约时间：' + yuyueshijian + ',' + dateType
        #post_info_map = {'tsname' : tsname, 'tsuserid' : tsuserid, 'marketemail' : marketemail,
        #                 'tsphone' : tsphone, 'wangqianhetong' : wangqianhetong, 'kehuxingming' : kehuxingming,
        #                 'kehushengfenzheng' : kehushengfenzheng, 'guohuzhuanyuan' : guohuzhuanyuan, 'yuyueshijian' : yuyueshijian,
        #                 'dateType' : dateType, 'svpdUpLoadType' : svpdUpLoadType, 'spvdName' : spvdName,
        #                 'svpdUpLoadTypeDetail' : svpdUpLoadTypeDetail, 'spvdCode' : spvdCode, 'svpdDetailCategory': svpdDetailCategory,
        #                 'checkBoxProduct' : checkBoxProduct, 'eoContent' : eoContent,  'post_account' : post_account}
        post_info_map = {'tsname' : tsname, 'tsuserid' : tsuserid, 'marketemail' : marketemail,
                         'tsphone' : tsphone, 'wangqianhetong' : wangqianhetong, 'kehuxingming' : kehuxingming,
                         'kehushengfenzheng' : kehushengfenzheng, 'guohuzhuanyuan' : guohuzhuanyuan, 'yuyueshijian' : yuyueshijian,
                         'dateType' : dateType, 'svpdUpLoadType' : svpdUpLoadType, 'spvdName' : spvdName,
                         'svpdUpLoadTypeDetail' : svpdUpLoadTypeDetail, 'spvdCode' : spvdCode, 'svpdDetailCategory': svpdDetailCategory,
                         'checkBoxProduct' : checkBoxProduct, 'eoContent' : eoContent}
        post_map.append(post_info_map)
        #print post_info_map
    #print post_map
    return post_map

def dongchengjiaoshui():
    jsessionid = get_jsessionid_from_file()
    print 'jsessionid is:' + jsessionid
    dongchengjiaoshui_addtocart(jsessionid)
    cart_info = dongchengjiaoshui_getuserinfo(jsessionid)
    parse_cart_info(cart_info)
    post_datas = get_dongchengjiaoshui_post_datas()
    #while True:
    removed_datas = []
    for post_data in post_datas:
        for account in accounts:
            post_data['post_account'] = account
            #print post_data['wangqianhetong']
            #if post_data['wangqianhetong'] == '32133':
            #    removed_datas.append(post_data)
            if dongchengjiaoshui_submitorder(jsessionid, post_data) == '1':
                removed_datas.append(post_data)
                dongchengjiaoshui_addtocart(jsessionid)
                break
    #print removed_datas
    post_datas = [data for data in post_datas if data not in removed_datas]
    #print post_datas

if __name__ == '__main__':
    db.connect_db()
    dongchengjiaoshui()
