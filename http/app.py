from urllib.parse import urlparse, urljoin

from flask import Flask, request, abort, make_response, json, jsonify, redirect, url_for, session
from jinja2.utils import generate_lorem_ipsum

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


@app.route('/foo3/')
def foo3():
    return f'<h1>Foo Page</h1><a href="{url_for("do_something")}">Do something and redirect</a>'


@app.route("/bar2/")
def bar2():
    return f'<h1>Bar Page</h1><a href="{url_for("do_something")}">Do something and redirect</a>'


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route('/do_something_and_redirect')
def do_something():
    return redirect_back()


# 校验URL的安全性
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/more/')
def more():
    # jinja2提供的随机生成文章内容的函数
    return generate_lorem_ipsum(n=2)


if __name__ == '__main__':
    app.run()
