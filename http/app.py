from flask import Flask, request

app = Flask(__name__)


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
    return '<h1>Hello, Flask!</h1>', 201


@app.route('/hello2/')
def hello2():
    return '', 302, {'Location': 'http://127.0.0.1:5000/go_back/2/'}


if __name__ == '__main__':
    app.run()
