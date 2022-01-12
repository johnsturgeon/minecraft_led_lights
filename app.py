import json
from threading import Thread

from flask import Flask, request, jsonify
from light_scene import LightScene
# from light_strip import blink_pixel, fill_color, rainbow_cycle
from light_strip import raining, stop_rain, sunset

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})


@app.route('/event', methods=['POST'])
def event():
    # blink_pixel(0)
    # fill_color(255, 255, 255)
    # rainbow_cycle(0)
    print(request.data)
    record = json.loads(request.data)
    if record['event'] == 'rainStarted':
        thread = Thread(target=raining)
        thread.start()
    elif record['event'] == 'rainStopped':
        stop_rain()
    elif record['event'] == 'sunsetStarted':
        sunset(0)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
