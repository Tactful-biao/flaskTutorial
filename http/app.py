from flask import Flask, request, abort, make_response, json, jsonify, redirect, url_for, session

app = Flask(__name__)

app.secret_key = 'fswerfg324y@$#^sdjks*&%^$#DSfsdsdsd'


@app.route('/')
def index():
    return 'Hello, Flask'


@app.route('/go_back/<int:year>/')
def go_back(year):
    return f'Welcome to {2022 - year}'


@app.route('/colors/<any(blue,red,white):color>/')
def three_colors(color):
    return f'This is a Beautiful Color - {str.upper(color)}'


colors = ['blue', 'white', 'red']


@app.route(f'/colors2/<any({colors}):color>/')
def colors(color):
    return f'This is a Beautiful Color - {str.upper(color)}'


# 在每次请求来临的时候输出hello
@app.before_request
def say_hello():
    print(request.path)


@app.route('/hello/')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = f'<h1>Hello, Flask!{name}</h1>'

        if 'login_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response, 201


@app.route('/hello2/')
def hello2():
    return '', 302, {'Location': 'http://127.0.0.1:5000/go_back/2/'}


@app.route('/404/')
def not_found():
    abort(404)


# 设置响应类型
@app.route('/foo/')
def foo():
    data = {
        'name': 'biao',
        'age': 26
    }
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response


# 针对json类型的响应，应该使用下面方式
@app.route('/foo2/')
def foo2():
    return jsonify(name='biao', age=25)


# 设置cookie
@app.route('/set/<name>/')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# 使用session模拟用户登录
@app.route('/login/')
def login():
    session['login_in'] = True  # 写入session
    return redirect(url_for('hello'))


# 模拟退出登录
@app.route('/logout/')
def logout():
    if 'login_in' in session:
        session.pop('login_in')
    return redirect(url_for('hello'))


# 模拟后台管理
@app.route('/admin/')
def admin():
    if 'login_in' not in session:
        abort(403)
    return 'Welcome to admin page!'


if __name__ == '__main__':
    app.run()
