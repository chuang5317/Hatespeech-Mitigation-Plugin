from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/getmethod', methods=['GET'])
def get_html_text():
    htmltext = request.json
    return jsonify({"response": "OK"})
