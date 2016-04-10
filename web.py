from flask import Flask
from flask import render_template
from flask import request
import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def init():
    main.get_jsessionid()
    main.get_captcha()
    return render_template('login.html')

#@app.route('/success', methods=['GET', 'POST'])
#def success():

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    username = None
    password = None
    captcha = None
    if request.method == 'POST':
        print 'Login method is Post'
        username = request.form.get('username')
        password = request.form.get('password')
        captcha = request.form.get('captcha')
    else:
        print 'Login method is Get'
        username = request.args.get('username')
        password = request.args.get('password')
        captcha = request.args.get('captcha')
    main.login(username, password, captcha)

@app.route('/addinfo', methods=['GET', 'POST'])
def add_info():
    fd = open('jsessionid.txt', 'r')
    jsessionid = fd.readline()
    fd.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
