#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from cognitive import emotions

app = Flask(__name__)
CORS(app)

@app.route('/collect', methods=['POST'])
@cross_origin()
def collect():
    if not request.json or 'image' not in request.json:
        abort(400)
    return jsonify({'response': emotions(request.json['image'])})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
