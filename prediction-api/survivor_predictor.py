import json
import os
import pickle
import pandas as pd
from flask import jsonify
import logging
from io import StringIO


class SurvivorPredictor:
    def __init__(self):
        self.model = None

    def load_model(self, file_path):
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)

    def predict_single_record(self, prediction_input):
        logging.debug(prediction_input)
        if self.model is None:
            try:
                model_repo = os.environ['MODEL_REPO'] #environment variable MODEL_REPO should point to the repo
                model_name = os.environ['MODEL_NAME']  #enviornment variable MODEL_NAME should specify the model, either lr_model.pckl or rf_model.pkl
                file_path = os.path.join(model_repo, model_name)
                with open(file_path, 'rb') as f:
                    self.model = pickle.load(f)
            except KeyError:
                print("MODEL_REPO or MODEL_NAME is undefined")
                exit()

        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        y_pred = self.model.predict(df)
        logging.info(y_pred[0])
        logging.info(str(y_pred[0]))
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(y_pred[0])}), 200
