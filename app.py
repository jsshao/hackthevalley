#!flask/bin/python
from flask import Flask, jsonify, request
from emotion import emotions

app = Flask(__name__)

@app.route('/collect', methods=['POST'])
def collect():
    if not request.json or not 'url' in request.json:
        abort(400)
    return jsonify({'response': emotions(request.json['url'])})

if __name__ == '__main__':
    app.run(debug=True)
