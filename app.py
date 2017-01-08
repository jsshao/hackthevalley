#!flask/bin/python
import json
from flask import Flask, jsonify, request, render_template, send_from_directory, abort
from flask_cors import CORS, cross_origin
from cognitive import emotions, face
from db import insertMetric, insertUser, userExists, getAllVideoIds, getVideoMetrics, getDemographic
from apiclient.discovery import build

DEVELOPER_KEY = "AIzaSyAcNZjvkEVgF7b8l4Mwc5xUu-7r2yRh8m4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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


@app.route('/admin/<string:video_id>', methods=['GET'])
@cross_origin()
def admin(video_id):
    return render_template("admin.html", video_id=video_id)


@app.route('/video/<string:video_id>', methods=['GET'])
@cross_origin()
def video(video_id):
    return render_template("video.html", video_id=video_id)


@app.route('/select', methods=['GET'])
@cross_origin()
def select():
    video_ids = getAllVideoIds()
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    videos = []
    for video_id in video_ids:
        search_response = youtube.videos().list(
            id=video_id,
            part="snippet",
            maxResults=1
        ).execute()

        for search_result in search_response.get("items", []):
            video_title = search_result["snippet"]["title"]
            videos.append((video_id, video_title))
    return render_template("select.html", videos=videos)


@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    return render_template("search.html")


@app.route('/search_results', methods=['POST'])
@cross_origin()
def search_results():
    query_string = request.form.get("query_string", "")

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=query_string,
        part="id,snippet",
        maxResults=25
    ).execute()
    videos = []
    for search_result in search_response.get("items", []):
        if "videoId" in search_result["id"]:
            video_id = search_result["id"]["videoId"]
            video_title = search_result["snippet"]["title"]
            videos.append((video_id, video_title))

    return render_template("search_results.html", videos=videos)


@app.route('/js/<path:path>')
@cross_origin()
def send_js(path):
    return send_from_directory('templates/js', path)


@app.route('/css/<path:path>')
@cross_origin()
def send_css(path):
    return send_from_directory('templates/css', path)
