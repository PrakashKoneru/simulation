import flask
from flask import request, jsonify
from flask_cors import CORS
from paisa_module import api_run_simulation

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route("/simulate", methods=["POST"])
def run_simulations():
    formData = request.get_json().get("formData")
    simulation_result = api_run_simulation(formData)
    print(simulation_result)
    return jsonify(simulation_result)


app.run()
