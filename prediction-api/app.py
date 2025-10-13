import os

from flask import Flask, request

from survivor_predictor import SurvivorPredictor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/survivor_predictor/', methods=['POST']) # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_input = request.get_json()
    return sp.predict_single_record(prediction_input)


sp = SurvivorPredictor()
if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5002)), host='0.0.0.0', debug=True)

