# flaskTutorial
```python
# 路由指定默认值
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
  return f'Hello, {name}'
```

## flask命令

```python
# 通过flask hello执行命令, 也可以在command中自定义命令名
@app.cli.command()
def hello():
  click.echo('Hello, Human!')
```

