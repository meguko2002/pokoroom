from flask import Flask, request, session, redirect, render_template
import socket

HOST = socket.gethostname()
PORT = 5000


app = Flask(__name__)
app.secret_key = '951951'

USERLIST = {
    'poko@gmail.com': 'poko',
    'hanako@yahoo.co.jp': 'bbb',
    'meguko2002@gmail.com': 'meguko',
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_login', methods=['POST'])
def check_login():
    user, pw = (None, None)
    if 'user' in request.form:
        user = request.form['user']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (user is None) or (pw is None):
        return redirect('/')
    if not try_login(user, pw):
        return """
        <h1>ユーザー名かパスワードが違っています</h1>
        <p><a href="/">→戻る</p>
        """
    return redirect('/private')


@app.route('/private')
def private_page():
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">→ログインする</a></p>
        """
    return render_template('private.html')


@app.route('/logout')
def logout_page():
    try_logout()
    return """
    <h1>ログアウトしました</h1>
    <p><a href="/">→戻る</a><p>
    """


def is_login():
    if 'login' in session:
        return True
    return False


def try_login(user, password):
    if not user in USERLIST:
        return False
    if USERLIST[user] != password:
        return False
    session['login'] = user
    return True


def try_logout():
    session.pop('login', None)
    return True


if __name__ == '__main__':
    app.run(host=HOST, port=PORT,debug=True)
