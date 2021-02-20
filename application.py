import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/simulate', methods=['GET'])
def run_simulations():
    id = int(request.args['id'])
    response = {
        "id" : id + 1
    }
    return jsonify(response)

app.run()