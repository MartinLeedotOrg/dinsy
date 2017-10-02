#!/usr/bin/env python3

import json
import datetime
from flask import Flask, request, Response, render_template

app = Flask(__name__)

data = {}


def on_get(self, req, resp):
    resp.body = json.dumps(data, ensure_ascii=False)


@app.route('/payload', methods=['POST'])
def payload():
    content = request.json
    client = content['this_host']
    output = content['results']
    data[client] = {}
    data[client]['output'] = output
    data[client]['datetime'] = str(datetime.datetime.now())
    return Response(None, status=202, mimetype='application/json')


@app.route('/', methods=['GET'])
def results():
    return render_template('results.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)