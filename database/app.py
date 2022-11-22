import os

import click
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref

app = Flask(__name__)

db = SQLAlchemy(app)

# 迁移文件
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'sqlite:////Users/sunshibiao/PycharmProjects/flaskTutorial/database/foo.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return f'<Note {self.body}>'


# 一对多外键定义
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    phone = db.Column(db.String(20))

    # 定义关系
    articles = db.relationship('Article')

    def __repr__(self):
        return f'<Author {self.name}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return f'<Article {self.title}>'


# 双向关系定义 back_populates 显示定义(推荐)
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    books = db.relationship('Books', back_populates='writer')

    def __repr__(self):
        return f'<Writer {self.name}>'


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')

    def __repr__(self):
        return f'<Book {self.title}>'


# 双向关系定义backref隐式定义
class Singer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)

    # 隐式定义双向关系，相当于在Song中定义了一个隐式的sing字段
    songs = db.relationship('Song', backref=backref('sing', uselist=False))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'))


# 多对一对关系
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City')

    def __repr__(self):
        return f'<Citizen {self.name}>'


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f'<City {self.name}>'


# 一对一对关系
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    capital = db.relationship('Capital', uselist=False)

    def __repr__(self):
        return f'<Country {self.name}>'


class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', overlaps="capital")

    def __repr__(self):
        return f'<Capital {self.name}>'


# 多对多关系
association_table = db.Table('association',
                             db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                             db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher', secondary=association_table, back_populates='students')


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    office = db.Column(db.String(20))

    students = db.relationship('Student', secondary=association_table, back_populates='teachers')


# 事件监听
class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)


@db.event.listens_for(Draft.body, 'set')
def increment_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1


# 自定义初始化数据库的命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    '''Initialize the database.'''
    if drop:
        click.confirm('This operation will delete the database, do you want to execute?')
        db.drop_all()
        click.echo("Drop tables.")
    db.create_all()
    click.echo('Initialized database.')


@app.route('/new/', methods=['GET', 'POST'])
def new_note():
    body = request.json.get('body')
    note = Note(body=body)
    db.session.add(note)
    db.session.commit()
    return 'OK', 201


@app.route('/')
def index():
    note = [x.body for x in Note.query.all()]
    return jsonify(note)


# 注册shell上下文
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Author=Author, Article=Article, Draft=Draft, Writer=Writer, Books=Books, Country=Country, Capital=Capital)
