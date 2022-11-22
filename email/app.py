import os
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('BIAO', os.getenv('MAIL_PASSWORD'))
)

mail = Mail(app)


# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


def send_mail(subject, to, body):
    message = Message(subject=subject, recipients=[to], body=body)
    mail.send(message)

