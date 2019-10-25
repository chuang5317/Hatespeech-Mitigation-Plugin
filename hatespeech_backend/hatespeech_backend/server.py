from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/postmethod', methods=['POST'])
def get_post_html_text():
    htmltext = request.form['data']
    return htmltext
