import click
from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/hi/')
def hello_world():  # put application's code here
    return '<h1>Hello World!</h1>'


@app.route('/greet/', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def get_name(name):
    return f'hello, {name}'

@app.cli.command()
def hello():
    click.echo('Hello, Human!')


if __name__ == '__main__':
    app.run()
