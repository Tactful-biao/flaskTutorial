from sayhi.sayhello import app
from sayhi.sayhello.models import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    data = Message.query.all()
    print()
    return ''