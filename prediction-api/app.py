import os
import requests
from flask import Flask, request, jsonify
from survivor_predictor import SurvivorPredictor

app = Flask(__name__)
app.config["DEBUG"] = True


WEBHOOK_BASE_URL = os.environ['CLOUDBUILD_WEBHOOK_BASE_URL']
SECRET_KEY = os.environ['CLOUDBUILD_SECRET_KEY']

@app.route('/survivor_predictor', methods=['POST']) # path of the endpoint. Accepts only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    try:
        prediction_input = request.get_json()
    except:
        return jsonify({
            "error": "Invalid or missing JSON payload."
        }), 400

    return sp.predict_single_record(prediction_input)

@app.post("/run_pipeline")
def run_pipeline():
    body = request.get_json(silent=True)
    api_key = request.headers.get("X-goog-api-key")
    url = f"{WEBHOOK_BASE_URL}&secret={SECRET_KEY}"
    headers = {
    # best practice for API security
    "X-goog-api-key": f'{api_key}'
    }

    req = requests.post(url, headers=headers, json=body, timeout=30)
    return jsonify(req.json()), req.status_code

sp = SurvivorPredictor()
if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5000)), host='0.0.0.0', debug=True)

