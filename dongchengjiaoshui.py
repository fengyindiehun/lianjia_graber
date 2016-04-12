# coding:utf-8

import urllib
import urllib2
import gevent
from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
import sys
import db
import util


#####################################################################
#GLOBAL VAR FOR USER
#####################################################################
tsname = None
tsuserid = None
marketemail = None
tsphone = None
account = None
#####################################################################


#####################################################################
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

def dongchengjiaoshui_get_user_pay_account():
    jsessionid = util.get_jsessionid_from_file()
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
    soup = BeautifulSoup(html_content, 'html.parser')
    for item in soup.find_all(name='input', attrs={'name':'post_account'}):
        #only return personal account
        return item.get('value').encode('utf-8')

def dongchengjiaoshui_parse_user_info(user_info_html):
    global tsname
    global tsuserid
    global marketemail
    global tsphone
    global account

    soup = BeautifulSoup(user_info_html, 'html.parser', from_encoding='latin-1')
    tsname = soup.find(id='post_user_input').get('value').encode('utf-8')
    tsuserid = soup.find(id='post_uid_input').get('value').encode('utf-8')
    marketemail = soup.find(name='input', attrs={'name':'marketemail'}).get('value').encode('utf-8')
    tsphone = soup.find(id='post_phone_input').get('value').encode('utf-8')
    account = dongchengjiaoshui_get_user_pay_account()

    print 'tsname:' + tsname
    print 'tsuserid:' + tsuserid
    print 'marketemail:'+ marketemail
    print 'tsphone:' + tsphone
    print 'account' + account

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
    if html_content == '1':
        print 'http://bjxwgl.homelink.com.cn/product/product_addTSProductToCart.action success'
    else:
        print 'http://bjxwgl.homelink.com.cn/product/product_addTSProductToCart.action failed, error_code is:' + html_content

def dongchengjiaoshui_submitorder(jsessionid, form_data, order_info):
    url = 'http://bjxwgl.homelink.com.cn/order/order_payOrderTSByAccount.action'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'JSESSIONID=' + jsessionid))
    data_encoded = urllib.urlencode(form_data)
    print 'dongchengjiaoshui form_data:' + data_encoded
    fd_read = opener.open(url, data_encoded)
    html_content = fd_read.read()
    if html_content == '1':
        print 'http://bjxwgl.homelink.com.cn/order/order_payOrderTSByAccount.action success, contract sd:' + form_data['wangqianhetong'] + ' success, '
        order_info[6] = '1'
        db.dongchengjiaoshui_update(order_info)
        dongchengjiaoshui_addtocart(jsessionid)
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

def dongchengjiaoshui_async(jsessionid, post_info, order_info):
    threads = []
    for i in range(1,10):
        threads.append(gevent.spawn(dongchengjiaoshui_submitorder, jsessionid, post_info, order_info))
    gevent.joinall(threads)

def dongchengjiaoshui():
    jsessionid = util.get_jsessionid_from_file()
    print 'jsessionid is:' + jsessionid
    dongchengjiaoshui_addtocart(jsessionid)
    user_info_html = dongchengjiaoshui_getuserinfo(jsessionid)
    dongchengjiaoshui_parse_user_info(user_info_html)

    for order_info in db.dongchengjiaoshui_select():
        if order_info[6] != '0':
            continue
        wangqianhetong = order_info[0]
        kehuxingming = order_info[1]
        kehushengfenzheng = order_info[2]
        guohuzhuanyuan = order_info[3]
        yuyueshijian = order_info[4]
        dateType = order_info[5]
        svpdUpLoadType = '-1'
        spvdName = '东城预约缴税'
        svpdUpLoadTypeDetail = '-1'
        spvdCode = 'ZN0870'
        svpdDetailCategory = '101336'
        checkBoxProduct = '2925_2188_2566'
        eoContent = '网签合同号：' + wangqianhetong + ',客户姓名：' + kehuxingming + ',身份证号：' + kehushengfenzheng + ',过户专员：' + guohuzhuanyuan + ',预约时间：' + yuyueshijian + ',' + dateType
        post_info = {'tsname' : tsname, 'tsuserid' : tsuserid, 'marketemail' : marketemail,
                     'tsphone' : tsphone, 'wangqianhetong' : wangqianhetong, 'kehuxingming' : kehuxingming,
                     'kehushengfenzheng' : kehushengfenzheng, 'guohuzhuanyuan' : guohuzhuanyuan, 'yuyueshijian' : yuyueshijian,
                     'dateType' : dateType, 'svpdUpLoadType' : svpdUpLoadType, 'spvdName' : spvdName,
                     'svpdUpLoadTypeDetail' : svpdUpLoadTypeDetail, 'spvdCode' : spvdCode, 'svpdDetailCategory': svpdDetailCategory,
                     'checkBoxProduct' : checkBoxProduct, 'eoContent' : eoContent, 'post_account' : account}
        dongchengjiaoshui_async(jsessionid, post_info, order_info)


if __name__ == '__main__':
    db.connect_db()
    dongchengjiaoshui()
