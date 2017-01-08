#!flask/bin/python
import json
from flask import Flask, jsonify, request, render_template, send_from_directory, abort
from flask_cors import CORS, cross_origin
from cognitive import emotions, face
from db import insertMetric, insertUser, userExists
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

context = (dir_path + '/cert/cert.pem', dir_path + '/cert/key.pem')

app = Flask(__name__)
CORS(app)


@app.route('/collect', methods=['POST'])
@cross_origin()
def collect():
    expectedFields = ['image', 'timestamp', 'video_id', 'user_id']
    if not request.json or not all(field in request.json for field in expectedFields):
        abort(400)

    if not userExists(request.json['user_id']):
        response = json.loads(face(request.json['image']))
        if len(response) == 0:
            abort(500)
        attributes = response[0]['faceAttributes']
        insertUser(request.json['user_id'], attributes['age'], attributes['gender'])

    response = json.loads(emotions(request.json['image']))
    if len(response) == 0:
        abort(500)
    scores = response[0]['scores']
    insertMetric(request.json['video_id'],
                 request.json['user_id'],
                 request.json['timestamp'],
                 scores['anger'],
                 scores['contempt'],
                 scores['disgust'],
                 scores['fear'],
                 scores['happiness'],
                 scores['neutral'],
                 scores['sadness'],
                 scores['surprise'])

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/admin', methods=['GET'])
@cross_origin()
def admin():
    return render_template("admin.html")


@app.route('/video', methods=['GET'])
@cross_origin()
def video():
    return render_template("video.html")


@app.route('/js/<path:path>')
@cross_origin()
def send_js(path):
    return send_from_directory('templates/js', path)


@app.route('/css/<path:path>')
@cross_origin()
def send_css(path):
    return send_from_directory('templates/css', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context=context)
