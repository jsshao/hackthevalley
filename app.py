#!flask/bin/python
from flask import Flask, jsonify, request, render_template, send_from_directory
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
    app.run(debug=True, host='0.0.0.0')
