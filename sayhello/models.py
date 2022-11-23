from datetime import datetime
from sayhi.sayhello import db


class Message(db.Model):
    '''模型类'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Message {self.name}>'