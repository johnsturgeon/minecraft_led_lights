import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})


@app.route('/event', methods=['POST'])
def event():
    record = json.loads(request.data)


if __name__ == '__main__':
    app.run()
