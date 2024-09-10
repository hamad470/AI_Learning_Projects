import pandas as pd
from flask import jsonify

class Model:
    def __init__(self, open=None, low=None, close=None, adj=None, volume=None):
        self.open = open
        self.low = low
        self.close = close
        self.adj = adj
        self.volume = volume

    def sign_up(self, df, new_row):
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("userdata.csv", index=False)
        return jsonify("Your account has been created successfully")

class BitcoiModel:
    def predict(self):
        # Placeholder for the model prediction logic
        return jsonify({"prediction": "Prediction result goes here"})


