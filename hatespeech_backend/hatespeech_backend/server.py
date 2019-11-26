from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/getmethod', methods=['GET'])
def get_html_text():
    htmltext = request.json
    return jsonify({"response": "OK"})


@app.route('/hatespeech', methods=['POST'])
def get_hatespeech():
    data = request.json
    nodes = data["nodes"]

    print(nodes)

    # Expect a list of [{"id": <int>, "text": <str>}]
    results = []
    for i, node in enumerate(nodes):
        # "hatespeech" value to be replaced by NLP engine's decision
        res = {"id": node["id"], "hatespeech": i % 2 == 0}
        results.append(res)

    return jsonify({"result": results})
