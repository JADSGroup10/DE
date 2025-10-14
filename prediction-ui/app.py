# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/checksurvivor', methods=["GET", "POST"])
def checksurvivor():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        prediction_input = [
            {
                "Pclass": int(request.form.get("class")),
                "Sex": request.form.get("sex"),
                "Age": int(request.form.get("age")),
                "no_of_siblings_or_partners_onboard": int(request.form.get("no_of_siblings_or_partners_onboard")),
                "no_of_parents_or_children_onboard": int(request.form.get("no_of_parents_or_children_onboard")),
            }
        ]

        if prediction_input[0]["Sex"].lower() == "male":
            prediction_input[0]["Sex"] = 0
        elif prediction_input[0]["Sex"].lower() == "female":
            prediction_input[0]["Sex"] = 1

        app.logger.debug("Prediction input : %s", prediction_input)


        predictor_api_url = os.environ['PREDICTOR_API']
        res = requests.post(predictor_api_url, json=json.loads(json.dumps(prediction_input)))

        prediction_value = res.json()['result']
        app.logger.info("Prediction Output : %s", prediction_value)

        
        return render_template("response_page.html",
                               prediction_variable=int(prediction_value))

    else:
        return jsonify(message="Method Not Allowed"), 405  


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
