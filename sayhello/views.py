from sayhello import app, db
from sayhello.models import Message
from flask import jsonify, request


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        data = Message.query.order_by(-Message.id).all()

        result = list()
        for x in data:
            temp = {
                'name': x.name,
                'body': x.body,
                'timestamp': x.timestamp
            }
            result.append(temp)
        return jsonify(result), 200
    elif request.method == 'POST':
        name = request.json.get('name')
        body = request.json.get('body')

        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()

        return 'OK', 201


