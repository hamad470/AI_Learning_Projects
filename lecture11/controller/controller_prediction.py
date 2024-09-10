from flask import jsonify
import pandas as pd
from model.model import BitcoiModel, Model

class PredictionController:
    
    
    def __init__(self, request):
        self.open = request.form.get('Open')
        self.close = request.form.get('Close')
        self.low = request.form.get('Low')
        self.adj = request.form.get('Adj Volume')
        self.volume = request.form.get('Volume')
        self.response = None
        try:
            self.df = pd.read_csv("userdata.csv")
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["ID", "Name", "Email", "Password"])
    def login(self, name, email, password):
        

        if self.validate_data():
            self.response = self.prediction()
        else:
            self.response = jsonify("Inputs are not validated")
    def iniit_df(self):
        
        if email in self.df.index:
            row = self.df.loc[email]
            if row['Name'] == name and row['Password'] == password:
                return jsonify(f"Welcome {name}")
            else:
                return jsonify("User email or password is incorrect")
        else:
            return jsonify("User email or password is incorrect")

    def sign_up(self, name, email, password):
        if email not in self.df.index:
            new_id = self.df['ID'].max() + 1
            new_row = pd.DataFrame({
                'ID': [new_id],
                'Name': [name],
                'Email': [email],
                'Password': [password]
            })
            model = Model()
            return model.sign_up(self.df, new_row)
        else:
            return jsonify("The email is already taken")

    def validate_data(self):
        try:
            if not all(isinstance(float(x), (int, float)) for x in [self.open, self.close, self.low, self.adj, self.volume]):
                return False
            return all(float(x) <= 234000 for x in [self.open, self.close, self.low, self.adj, self.volume])
        except ValueError:
            return False

    def prediction(self):
        self.preprocess()
        model = BitcoiModel()
        return model.predict()

    def preprocess(self):
        
        pass
