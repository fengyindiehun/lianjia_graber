from flask import Flask
from flask import render_template
from flask import request
import main
import db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def init():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/dologin', methods=['GET', 'POST'])
def dologin():
    main.get_jsessionid()
    main.get_captcha()
    username = None
    password = None
    captcha = None
    if request.method == 'POST':
        print 'Login method is Post'
        username = request.form.get('username').encode('utf-8')
        password = request.form.get('password').encode('utf-8')
        captcha = request.form.get('captcha').encode('utf-8')
    else:
        print 'Login method is Get'
        username = request.args.get('username').encode('utf-8')
        password = request.args.get('password').encode('utf-8')
        captcha = request.args.get('captcha').encode('utf-8')

    main.user_login(username, password, captcha)
    return render_template('index.html')

@app.route('/dongchengjiaoshui_add', methods=['GET', 'POST'])
def dongchengjiaoshui_add():
    return render_template('dongchengjiaoshui_add.html')

@app.route('/dodongchengjiaoshui_add', methods=['GET', 'POST'])
def dodongchengjiaoshui_add():
    hetonghao = None
    kehuxingming = None
    shenfenzheng = None
    guohuzhuanyuan = None
    status = '0'
    if request.method == 'POST':
        print 'dodongchengjiaoshui_add method is Post'
        hetonghao = request.form.get('hetonghao').encode('utf-8')
        kehuxingming = request.form.get('kehuxingming').encode('utf-8')
        shenfenzheng = request.form.get('shenfenzheng').encode('utf-8')
        guohuzhuanyuan = request.form.get('guohuzhuanyuan').encode('utf-8')
        yuyueshijian = request.form.get('yuyueshijian').encode('utf-8')
        shijianduan = request.form.get('shijianduan').encode('utf-8')
    else:
        print 'dodongchengjiaoshui_add method is Get'
        hetonghao = request.args.get('hetonghao').encode('utf-8')
        kehuxingming = request.args.get('kehuxingming').encode('utf-8')
        shenfenzheng = request.args.get('shenfenzheng').encode('utf-8')
        guohuzhuanyuan = request.args.get('guohuzhuanyuan').encode('utf-8')
        yuyueshijian = request.args.get('yuyueshijian').encode('utf-8')
        shijianduan = request.args.get('shijianduan').encode('utf-8')

    db.connect_db()
    db.dongchengjiaoshui_insert((hetonghao, kehuxingming, shenfenzheng, guohuzhuanyuan, yuyueshijian, shijianduan, status))
    return render_template('index.html')

@app.route('/dongchengguohu_add', methods=['GET', 'POST'])
def dongchengguohu_add():
    return render_template('dongchengguohu_add.html')

@app.route('/dodongchengguohu_add', methods=['GET', 'POST'])
def dodongchengguohu_add():
    hetonghao = None
    kehuxingming = None
    shenfenzheng = None
    guohuzhuanyuan = None
    status = '0'
    if request.method == 'POST':
        print 'dodongchengguohu_add method is Post'
        shoumaixingming = request.form.get('shoumaixingming').encode('utf-8')
        goumaixingming = request.form.get('goumaixingming').encode('utf-8')
        hetonghao = request.form.get('hetonghao').encode('utf-8')
        qishuipiaohao = request.form.get('qishuipiaohao').encode('utf-8')
        guohuzhuanyuan = request.form.get('guohuzhuanyuan').encode('utf-8')
        yuyueshijian = request.form.get('yuyueshijian').encode('utf-8')
        shijianduan = request.form.get('shijianduan').encode('utf-8')
    else:
        print 'dodongchengguohu_add method is Get'
        shoumaixingming = request.args.get('shoumaixingming').encode('utf-8')
        goumaixingming = request.args.get('goumaixingming').encode('utf-8')
        hetonghao = request.args.get('hetonghao').encode('utf-8')
        qishuipiaohao = request.args.get('qishuipiaohao').encode('utf-8')
        guohuzhuanyuan = request.args.get('guohuzhuanyuan').encode('utf-8')
        yuyueshijian = request.args.get('yuyueshijian').encode('utf-8')
        shijianduan = request.args.get('shijianduan').encode('utf-8')

    db.connect_db()
    db.dongchengguohu_insert((shoumaixingming, goumaixingming, hetonghao, qishuipiaohao, guohuzhuanyuan, yuyueshijian, shijianduan, status))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
