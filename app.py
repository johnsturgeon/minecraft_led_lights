import json
from flask import Flask, request, jsonify
from light_strip import blink_pixel

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})


@app.route('/event', methods=['POST'])
def event():
    blink_pixel(0)
    record = json.loads(request.data)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
