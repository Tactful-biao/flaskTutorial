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

## Flask中request的相关信息

+ http://baidu.com/query?k=biao

+ 使用request的属性获取请求URL

| 属性      | 值                   | 属性     | 值                               |
| --------- | -------------------- | -------- | -------------------------------- |
| path      | u'/query'            | base_url | u'http://baidu.com/query'        |
| full_path | u'/query?k=biao'     | url      | u'http://baidu.com/query?k=biao' |
| host      | u'baidu.com'         | url_root | u'http://baidu.com/'             |
| host_url  | u'http://baidu.com/' |          |                                  |

+ request对象常用的属性和方法

|                        属性/方法                         |                             说明                             |
| :------------------------------------------------------: | :----------------------------------------------------------: |
|                           args                           | Werkzeug的ImmutableMultiDict对象。存储解析后的查询字符串，可通过字典方式获取键值。如果你想获取未解析的原声字符串，可以使用query_string属性。 |
|                        blueprint                         |                        当前蓝图的名称                        |
|                         cookies                          |           一个包含所有随机请求提交的cookies的字典            |
|                           data                           |                   包含字符串形式的请求数据                   |
|                         endpoint                         |                   与当前请求相匹配的端点值                   |
|                          files                           | Werkzeug的MultiDict对象，包含所有上传文件，可以使用字典的形式获取文件。使用的键为文件input标签中的name属性值，对应的值为Werkzeug的FileStore对象，可以调用save()方法并传入保存路径来保存文件。 |
|                           form                           | Werkzeug的MultiDict对象。与files类似，包含解析后的表单数据。表单字段通过input标签的name属性值作为键获取。 |
|                          values                          | Werkzeug的ImmutableMultiDict对象，结合了args和form属性的值。 |
| get_data(cache=True,as_text=False,parse_form_data=False) | 获取请求中的数据，默认读取为字节字符串(bytestring)，将as_text设为True则返回值将是解码后的unicode字符串。 |
|    get_json(self,force=False,silent=False,cache=True)    | 将JSON解析并返回数据，如果MIME类型不是JSON，返回None(除非force设为True)；解析出错则跑出Werkzeug提供的BadRequest异常(如果未开启调试模式，则返回400错误响应)如果silent设置为True则返回None；cache设置是否缓存解析后的JSON数据。 |
|                         headers                          | 一个Werkzeug的EnvironHeaders对象，包含首部字段，可以以字典的形式操作 |
|                         is_json                          |          通过MIME类型判断是否为JSON数据，返回布尔值          |
|                           json                           | 包含解析后的JSON数据，内部调用get_json()，可通过字典的方式获取键值 |
|                          method                          |                        请求的HTTP方法                        |
|                         referrer                         |                 请求发起的源URL，即referrer                  |
|                          scheme                          |                  请求的URL模式(http或https)                  |
|                        user_agent                        | 用户代理(User Agent, UA)，包含了用户的客户端类型，操作系统类型等信息。 |

+ Flask内置的URL变量转换器

| 转换器 |                             说明                             |
| :----: | :----------------------------------------------------------: |
| string |                  不包含斜线的字符串(默认值)                  |
|  int   |                             整型                             |
| float  |                            浮点数                            |
|  path  | 包含斜线的字符串。static路由的URL规则中的filename变量就使用了这个转换器 |
|  any   |                 匹配一系列给定值中的一个元素                 |
|  uuid  |                          UUID字符串                          |

+ flask请求钩子

|         钩子         |                             说明                             |
| :------------------: | :----------------------------------------------------------: |
| before_first_request |             注册一个函数，在处理第一个请求前运行             |
|    before_request    |              注册一个函数，在处理每个请求前运行              |
|    after_request     | 注册一个函数，如果没有未处理的异常跑出，会在每个请求结束后运行 |
|   teardown_request   | 注册一个函数，即使有未处理的异常抛出，会在每个请求结束后运行。如果发生异常，会传入异常对象作为参数到注册的函数中。 |
|  after_this_request  |      在视图函数内注册一个函数，会在这个请求结束后运行。      |

+ 常见的HTTP状态码

| 类型         | 状态码 | 原因短语(用于解释状态码) | 说明                                                         |
| ------------ | :----: | ------------------------ | ------------------------------------------------------------ |
| 成功         |  200   | OK                       | 请求被正常处理                                               |
| 成功         |  201   | Created                  | 请求被处理，并创建了一个新资源                               |
| 成功         |  204   | No Content               | 请求处理成功，但无内容返回                                   |
| 重定向       |  301   | Moved Permanently        | 永久重定向                                                   |
| 重定向       |  302   | Found                    | 临时性重定向                                                 |
| 重定向       |  304   | Not Modified             | 请求的资源未被修改，重定向到缓存的资源                       |
| 客户端错误   |  400   | Bad Request              | 表示请求无效，即请求报文中存在错误                           |
| 客户端错误   |  401   | Unauthorized             | 类似403，表示请求的资源需要获取授权信息，在浏览器中会弹出认证弹窗 |
| 客户端错误   |  403   | Forbidden                | 表示请求的资源被服务器拒绝访问                               |
| 客户端错误   |  404   | Not Found                | 表示服务器上无法找到请求的资源或URL无效                      |
| 服务器端错误 |  500   | Internal Server Error    | 服务器内部发生错误                                           |

+ 在Flask中生成响应(响应主体，状态码，首部字段)

  ```python
  # 在返回响应的时候可以指定响应主体和响应状态码
  @app.route('/hello/')
  def hello():
    return '<h1>Hello, Flask</h1>', 201
  
  # 在重定向的时候可以设置重定向的目标
  @app.route('/hello/')
  def hello():
    return '', 302, {'Location', 'http://www.baidu.com'}
  ```

+ 重定向redirect

  ```python
  # redirect默认响应码是302，可以通过制定第二个参数来改变响应码
  @app.route('/hi/')
  def hi():
    return redirect(url_for('hello'))  # 重定向到/hello
  ```

+ abort()函数用于抛出指定的错误







