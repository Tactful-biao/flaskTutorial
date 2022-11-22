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

+ jsonify函数可以通过传参的方式生成json响应

  ```python
  from flask import jsonify
  
  # 方式一
  return jsonify(name='biao', age=27)
  
  # 方式二
  return jsonify({name='biao', age=27})
  
  # 可以指定返回的响应值
  return jsonify(message='Error!'), 500
  ```

+ Response类的常用属性和方法

  | 方法/属性   | 说明                                                        |
  | ----------- | ----------------------------------------------------------- |
  | headers     | 一个Werkzeug的Headers对象，表示响应首部，可以像字典一样操作 |
  | status      | 状态码，文本类型                                            |
  | status_code | 状态码，整型                                                |
  | mimetype    | MIME类型(仅包含内容类型部分)                                |
  | set_cookie  | 用来设置一个cookie                                          |

+ set_cookie方法的参数

  | 属性     | 说明                                                         |
  | -------- | ------------------------------------------------------------ |
  | key      | cookie的键(名称)                                             |
  | value    | cookie的值                                                   |
  | max_age  | cookie被保存的时间数，单位为秒；默认在用户回话结束(即关闭浏览器)时过期 |
  | expires  | 具体的过期时间，一个datetime对象或UNIX时间戳                 |
  | path     | 限制cookie只在给定的路径可用，默认为整个域名                 |
  | domain   | 设置cookie可用的域名                                         |
  | secure   | 如果设为True，只有通过HTTPS才可以使用                        |
  | httponly | 如果设置为True，禁止客户端JavaScript获取cookie               |

+ Flask中的上下文变量

  | 变量名      | 上下文类别 | 说明                                                         |
  | ----------- | ---------- | ------------------------------------------------------------ |
  | current_app | 程序上下文 | 指向处理请求的当前程序实例                                   |
  | g           | 程序上下文 | 替代Python的全局变量用法，确保仅在当前请求中可用。用于存储全局数据，每次请求都会重设 |
  | request     | 请求上下文 | 封装客户端发出的请求报文数据                                 |
  | session     | 请求上下文 | 用于记住请求之间的数据，通过签名的cookie实现                 |

+ ajax函数支持的参数

  | 参数        | 参数值类型及默认值                                           | 说明                                                       |
  | ----------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
  | url         | 字符串；默认为当前页地址                                     | 请求的地址                                                 |
  | type        | 字符串；默认为GET                                            | 请求方式                                                   |
  | data        | 字符串；无默认值                                             | 发送到服务器的数据                                         |
  | dataType    | 字符串；                                                     | 期待服务器返回的数据类型                                   |
  | contentType | 字符串；默认为'application/X-www-form-urlencoded;charset=UTF-8' | 发生请求时使用的内容类型，即请求首部的Content-Type字段内容 |
  | complate    | 函数；无默认值                                               | 请求完成后调用的回调函数                                   |
  | success     | 函数；无默认值                                               | 请求成功后调用的回调函数                                   |
  | error       | 函数；无默认值                                               | 请求失败后调用的回调函数                                   |

+ SQLAlchemy常用的字段类型

  | 字段        | 说明                                          |
  | ----------- | --------------------------------------------- |
  | Integer     | 整数                                          |
  | String      | 字符串，可选参数length可以用来设置最大长度    |
  | Text        | 较长的Unicode文本                             |
  | Date        | 日期，存储Python的datetime.date对象           |
  | DateTime    | 时间，存储Python的datetime.time对象           |
  | Time        | 时间和日期，存储python的datetime.datetime对象 |
  | Interval    | 时间间隔，存储python的datetime.timedelta对象  |
  | Float       | 浮点数                                        |
  | Boolean     | 布尔值                                        |
  | PickleType  | 存储Pickle列化的Python对象                    |
  | LargeBinary | 存储任意二进制数据                            |

+ 常用的SQLAlchemy字段参数

  | 参数名      | 说明                                              |
  | ----------- | ------------------------------------------------- |
  | primary_key | 如果设为True，该字段为主键                        |
  | unique      | 如果设为True，该字段不允许出现重复值              |
  | index       | 如果设为True，为该字段创建索引，以提高查询效率    |
  | nullable    | 确定字段值可否为空，值为True或False，默认值为True |
  | default     | 为字段设置默认值                                  |

+ SQLAlchemy的操作

  ```python
  # 插入操作
  from app import db, Note
  
  note1 = Note(body='Note1')
  note2 = Note(body='Note2')
  note3 = Note(body='Note3')
  
  db.session.add(note1)
  db.session.add(note2)
  db.session.add(note3)
  
  # 或者使用add_all()
  db.session.add_all([note1, note2, note3])
  
  db.session.commit()
  ```

+ SQLAlchemy常用的查询方法

  | 查询方法              | 说明                                                         |
  | --------------------- | ------------------------------------------------------------ |
  | all()                 | 返回包含所有查询记录的列表                                   |
  | first()               | 返回查询的第一条记录，如果未找到，返回None                   |
  | one()                 | 返回第一条记录，仅且运行有一条记录。如果记录数量大于1或小于1，则抛出错误 |
  | get(ident)            | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回None |
  | count()               | 返回查询结果的数量                                           |
  | one_or_none()         | 类型one(),如果结果数量不为1，返回None                        |
  | first_or_404()        | 返回查询的第一条记录，如果未找到返回None                     |
  | get_or_404(ident)     | 传入主键作为参数，返回指定主键值的记录，如果未找到，则返回404错误响应 |
  | paginate()            | 返回一个Pagination对象，可以对记录进行分页处理               |
  | with_parent(instance) | 传入模型类实例作为参数，返回和这个实例相关联的对象，后面会详细介绍 |

+ 常用的SQLAlchemy过滤方法

  | 查询过滤器名称 | 说明                                                         |
  | -------------- | ------------------------------------------------------------ |
  | filter()       | 使用指定的规则过滤记录，返回新产生的查询对象                 |
  | filter_by()    | 使用指定规则过滤记录(以关键字表达式的形式)，返回新产生的查询对象 |
  | order_by()     | 根据指定条件对记录进行排序，返回新产生的查询对象             |
  | limit(limit)   | 使用指定的值限制原查询返回的记录数量，返回新产生的查询对象   |
  | group_by()     | 根据指定条件对记录进行分组，返回新产生的查询对象             |
  | offset(offset) | 使用指定的值偏移原查询的结果，返回新产                       |

+ SQLAlchemy查询的例子

  ```python
  # 查询所有
  Note.query.all()
  
  # 查询指定
  Note.query.get(2)
  
  # 过滤查询
  Note.query.filter(Note.body=='ShAVE').first()
  
  # 打印查询对象可以转换成对应的SQL语句
  print(Note.query.filter(Note.body=='ShAVE'))
  
  # 模糊查询
  Note.query.filter(Note.body.like('%foo'))
  
  # in
  Note.query.filter(Note.body.in_(['foo', 'bar', 'baz']))
  
  # not in
  Note.query.filter(~Note.body.in_(['foo', 'bar', 'baz']))
  
  # AND 
  from sqlalchemy import and_
  Note.query.filter(and_(Note.body == 'foo', Note.title=='FooBar'))
  
  # AND 的另一种形式
  Note.query.filter(Note.body == 'foo', Note.title=='FooBar')
  
  # 叠加调用filter()/filter_by()方法
  Note.query.filter(Note.body == 'foo').filter(Note.title == 'FooBar')
  
  # OR
  from sqlalchemy import or_
  Note.query.filter(or_(Note.body == 'foo', Note.body == 'bar'))
  
  # filter_by的操作更加简单
  Note.query.filter_by(body='SHAVE').first()
  ```

+ Update操作

  ```python
  # 查出需要更改的数据
  note = Note.query.get(2)
  
  note.body = 'SHAVE LEFT THIGH'
  db.session.commit()
  ```

+ Delete操作

  ```python
  note = Note.query.get(2)
  
  db.session.delete(note)
  
  db.session.commit()
  ```


+ 注册Shell上下文，把db集成到shell启动中

  ```python
  @app.shell_context_processor
  def make_shell_context():
    return dict(db=db, Note=Note)
  ```

+ 定义外键

  + 针对一对多，外键要定义在“多”的一侧

  + 定义关系属性，需要在“一”的这一侧进行定义(相当于一个快捷查询，不会存入数据库)

    ```python
    # 可以通过关系属性查询或者添加关系
    foo.articles  # 返回关系集合结果
    
    # 添加关系
    foo.articles.append(spam)
    
    # 移除关系, remove, pop
    foo.articles.remove(spam)
    ```

  + 双向关系定义back_populations、backref区别

  + 多对一把关系和外键定义在“多”对一侧，本质和一对多一样

  + 一对一需定义双向关系，在关系定义中只能返回单条数据，在关系中需要定义uselist=False

  + 多对多关系需要定义一个关系表，需要定义双向关系和指定secondary参数，关系表SQLAlchemy会管理

    ```python
    association_table = db.Table('association', db.Column('student_id', db.Integer), db.Column('teacher_id', db.Integer))
    
    
    class Student(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(70), unique=True)
        grade = db.Column(db.String(20))
        teachers = db.relationship('Teacher', secondary=association_table, back_populates='students')
    
    
    class Teacher(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(70), unique=True)
        office = db.Column(db.String(20))
    
        students = db.relationship('Student', secondary=association_table, back_populations='teachers')s
    ```

+ 常用的SQLAlchemy关系函数参数

  | 参数名         | 说明                                                         |
  | -------------- | ------------------------------------------------------------ |
  | back_populates | 定义反向引用，用于建立双向关系，在关系的另一侧也必须显式定义关系属性 |
  | backref        | 添加反向引用，自动在另一侧建立关系属性，是back_populates的简化版 |
  | lazy           | 指定如何加载相关记录                                         |
  | uselist        | 指定是否使用列表的形式加载记录，设为False则使用标量(scakar)  |
  | cascade        | 设置级联操作                                                 |
  | order_by       | 指定加载相关记录时的排序方式                                 |
  | secondary      | 在多对多关系中指定关联表                                     |
  | primaryjoin    | 指定多对多关系中的一级联结条件                               |
  | secondaryjoin  | 指定多对多关系中的二级联结条件                               |

  

+ 常用的SQLAlchemy关系记录加载方式(lazy参数可选值)

  | 关系加载方式 | 说明                                                         |
  | ------------ | ------------------------------------------------------------ |
  | select       | 在必要时一次性加载记录，返回包含记录的列表(默认值)，等同于lazy=True |
  | joined       | 和父查询一样加载记录，但使用联结，等同于lazy=False           |
  | immediate    | 一旦父查询加载就加载                                         |
  | subquery     | 类似于joined，不过将使用子查询                               |
  | dynamic      | 不直接加载记录，而是返回一个包含相关记录的query对象，以便再继续附加查询函数对结果进行过滤 |

+ 数据库迁移
  + flask-migrate：内部集成了Migrate
  + flask db init 初始化数据库
  + flask db migrate -m "迁移文件" 生成迁移文件
  + flask db upgrade 更新到数据库
+ 级联操作 cascade(谨慎使用)
  + save-update、merge(默认值)
    + save-update相关联的两个对象都会同时添加到数据库会话中
  + save-update、metge、delete
    + delete：相关的对象会一起被删掉
  + all
  + all、delete-orphan
    + delete-orphan通常跟delete一起使用
    + 当父对象与子对象解除关系时，也会删除子对象

+ 事件监听

  + listen_for()装饰器，用于监听属性的事件标识符set、append、remove、init_scalar、init_collection

    ```python
    @db.event.listens_for(Draft.body, 'set')
    def increment_edit_time(target, value, oldvalue, initiator):
      if target.edit_time is not None:
        target.edit_time += 1
        
    @db.event.listerns_for(Draft.body, 'set', named=True)
    def increment_edit_time(**kwargs):
      if kwargs['target'].edit_time is not None:
        kwargs['target'].edit_time += 1
    ```

    





