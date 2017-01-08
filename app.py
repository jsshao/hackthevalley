#!flask/bin/python
import json
from flask import Flask, jsonify, request, render_template, send_from_directory, abort
from flask_cors import CORS, cross_origin
from cognitive import emotions, face
from db import insertMetric, insertUser, userExists, getAllVideoIds, getVideoMetrics, getDemographic

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
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        attributes = response[0]['faceAttributes']
        insertUser(request.json['user_id'], attributes['age'], attributes['gender'])

    response = json.loads(emotions(request.json['image']))
    if len(response) == 0:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
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


@app.route('/metric', methods=['POST'])
@cross_origin()
def metric():
    if not request.json or not 'video_id' in request.json:
        abort(400)
    return jsonify(getVideoMetrics(request.json['video_id']))

@app.route('/demographic', methods=['POST'])
@cross_origin()
def demographic():
    if not request.json or not 'video_id' in request.json:
        abort(400)
    return jsonify(getDemographic(request.json['video_id']))

@app.route('/all_videos', methods=['GET'])
@cross_origin()
def all_videos():
    return jsonify(getAllVideoIds())

@app.route('/admin', methods=['GET'])
@cross_origin()
def admin():
    return render_template("admin.html")

@app.route('/video', methods=['GET'])
@cross_origin()
def video():
    return render_template("video.html")


@app.route('/select', methods=['GET'])
@cross_origin()
def select():
    video_ids = getAllVideoIds()
    return render_template("select.html", video_ids=video_ids)

@app.route('/js/<path:path>')
@cross_origin()
def send_js(path):
    return send_from_directory('templates/js', path)


@app.route('/css/<path:path>')
@cross_origin()
def send_css(path):
    return send_from_directory('templates/css', path)
