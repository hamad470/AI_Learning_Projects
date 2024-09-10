from flask import Flask, request, render_template,jsonify
import pandas as pd
import numpy as np
from flask_cors import CORS
from bitcoin import CustomLinearRegression
import pickle
import datetime
import csv

app = Flask(__name__)
CORS(app)
import datetime

# Unix timestamp





# Convert timestamp to datetime


import pandas as pd

# Read the CSV file
df = pd.read_csv("dataset/data.csv")

# Drop unnecessary columns
df.drop(columns=["Weighted_Price", "Close"], inplace=True)

# Drop rows with any missing values
df.dropna(inplace=True)

# Sample 50 rows from the dataset
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='coerce')
df = df.sample(n=1000)

# Ensure the "Timestamp" column is correctly formatted as Unix time
# Convert Unix timestamps to readable dates (datetime64[ns])
# errors ="coerce" removes the elments causing error


# Sort the dataframe by the "Timestamp" column
df = df.sort_values(by='Timestamp')

# Convert the DataFrame to a NumPy array if needed
df = df.values

class Prediction_controller:
    def __init__(self):
        self.file_path ="dataset/data.csv"
        self.df = self.read_data(self.file_path)
        self.df = self.preprocess_data(self.df)
        self.prediction_permission =False
        self.limits =4
        self.subscribed_check =False

    def read_data(self,file_path):
        df = pd.read_csv(file_path)
        return df
    def preprocess_data(self,df):
        df.drop(columns=["Weighted_Price", "Close"], inplace=True)
        df.dropna(inplace=True)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='coerce')
        df = df.sample(n=1000)
        df = df.sort_values(by='Timestamp')
        df = df.values
        return df
    def pagination(self,request):
        page = request.args.get('page', 1, type=int)
        # Define the number of rows per page
        per_page = 20
        
        # Calculate the start and end indices for the current page
        start = (page - 1) * per_page
        end = start + per_page
        
        # Get the data for the current page
        page_data = df[start:end]
        
        # Calculate total number of pages
        total_pages = (len(self.df) + per_page - 1) // per_page
        
        # Determine the range of pages to display
        page_range = 10  # Number of page links to display
        start_page = max(1, page - page_range // 2)
        end_page = min(total_pages, start_page + page_range - 1)
        
        if end_page - start_page < page_range - 1:
            start_page = max(1, end_page - page_range + 1)
        return (page_data,page,total_pages,start_page,end_page,self.df)
    def standardize_x(self,X):
        obj = CustomLinearRegression()
        X[0][0] = (X[0][0] - obj.open_m) / obj.open_std
        X[0][1] = (X[0][1] - obj.low_m) / obj.low_std  
        X[0][2] = (X[0][2] - obj.btc_m) / obj.btc_std   
        X[0][3] = (X[0][3] - obj.vol_m) / obj.vol_std
        return X
    def receive_and_process_data(self,request):
        data = request.get_json()
        open_value = data.get("open")
        low_value = data.get("low")
        btc_value = data.get("btc")
        volume_value = data.get("vol")
        received_data = pd.DataFrame({"open":[open_value],
                            "low":[low_value],
                            "btc":[btc_value],
                            "volume":[volume_value]})
        X = received_data.values
        X = np.array(X, dtype=float)
        # print(X)
        X=self.standardize_x(X)
        return X
    def toggle(self,subs):
        return subs.apply(lambda x:not x )
    def subscribe(self):
        limits_path = "dataset/limits.csv"
        accounts = pd.read_csv("dataset/accounts.csv")
        limits = pd.read_csv(limits_path)
        if 'subscribed' in limits.columns:
            pass
        else:
            limits['subscribed']=False
        index = [i for i in accounts.index if accounts.loc[i,'signed_in']==True ]
        
        limits.loc[index,'subscribed']=self.toggle(limits.loc[index,'subscribed'])
        subs= limits.loc[index,'subscribed']
        print(subs)
        if subs.any():
            limits.to_csv(limits_path,index=False)
            self.limits+=4
            return "subscribed"
        else:
            limits.to_csv(limits_path,index=False)
            self.limits=0
            return "unsubscribed"
        
    def predict(self,input):
        if self.prediction_permission:
            if self.limits >0:
                obj1 = CustomLinearRegression()
                obj2 = obj1.load_model('lin_model.pkl')
                prediction = obj2.predict(input)
                # print(prediction)
                prediction =abs((prediction[0]*obj1.high_std+ obj1.high_m))
                # print(prediction)
                self.limits -=1
                return prediction
            else:
                message = "free trial ended, subscribe to get 4 more tries"
                return message
        else:
            message = "sign in for prediction"
            return message
    def account_exists(self,email):
        accounts = pd.read_csv("dataset/accounts.csv")
        count =0
        for e in accounts['email']:
            if email == e:
                count+=1
            else:
                continue
        if count>0:
            return False
        else:
            return True

    def register(self,request):
        if request.method == "POST":
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            pass1 = data.get('pass1')
            rpass = data.get('rpass')
            df_signup = {"name":[name],"email":[email],"pass1":[pass1],"rpass":[rpass]}
            if df_signup.get('pass1') == df_signup.get('rpass'):       
                accounts_path = "dataset/accounts.csv"
                limits_path = "dataset/limits.csv"
                

                if self.account_exists(email):
                    with open(accounts_path,mode="a",newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([name,email,pass1])
                    with open(limits_path,mode="a",newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([email,self.limits])
                    message = f"{name},your information is submitted succesfully"
                    return message
                else:
                    message = f"{email} already has account"
                    return message
            else:
                message = f"{name},there is password mismatch"
                return  message 
    def validate_sigin(self,request):
        accounts_path = "dataset/accounts.csv"
        signup_data = pd.read_csv(accounts_path)
        if 'signed_in' not in signup_data.columns:
            signup_data["signed_in"] =False
        if request.method == "POST":
            data = request.get_json()
            email = data.get('email')
            print(email)
            password = data.get('pass')
            if not self.account_exists(email):
                for i in signup_data.index:
                    if email == signup_data.loc[i,"email"] and password == signup_data.loc[i,"password"]:
                        signup_data.at[i,'signed_in']=True
                        signup_data.to_csv(accounts_path, index=False)
                        self.prediction_permission=True
                        message = "you are signed in"
                        return message
                else:
                    message = "password is not valid"
                    return message
                    

            else:
                message = f"{email} is not valid, enter valid email or create an account"
                return message

