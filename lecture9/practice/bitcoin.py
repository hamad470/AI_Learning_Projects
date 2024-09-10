import pandas as pd 
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
df = pd.read_csv("dataset/data.csv")
df.drop(columns =["Weighted_Price","Close","Timestamp"],inplace=True)

df.dropna(inplace=True)

class CustomLinearRegression:
    def __init__(self):
        self.df = df
        self.split_data()
        self.initialize_params()
        self.open_m =6009.023680
        self.open_std =8996.246106436112
        self.low_m =6004.488004
        self.low_std =8988.777075268166
        self.btc_m =9.323249
        self.btc_std =30.549887017246625
        self.vol_m =41762.842397
        self.vol_std =151824.7628942478
        self.high_m =6013.357082
        self.high_std =9003.519760651878
    def standardize_x(self, X):
        for i in range(len(X[0])):
            m = np.mean(X[:, i])
            std = np.std(X[:, i])
            X[:, i] = (X[:, i] - m) / std

    def standardize_y(self, y):
        m = np.mean(y)
        std = np.std(y)
        # if y = (y - m) / std it will create a new variable y and will not update original array,y-m subtract 
        #s from  each elemnt array 
        y[:] = (y - m) / std 

    def split_data(self):
        self.X=self.df[["Open","Low","Volume_(BTC)","Volume_(Currency)"]]
        self.y=self.df["High"]
        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X,self.y,random_state=42,test_size=0.2)
        self.X_train = np.array(self.X_train)
        self.standardize_x(self.X_train)
        self.y_train = np.array(self.y_train)
        self.standardize_y(self.y_train)
        self.standardize_y(self.y_train)
        self.X_test = np.array(self.X_test)
        self.standardize_x(self.X_test)
        self.y_test = np.array(self.y_test)
        self.standardize_y(self.y_test)
        
        
    def initialize_params(self):
        self.w = np.zeros(len(self.X_train[0]))
        self.b=0
        
        self.lr= 0.1
    def predict(self,X):
        predictions =[np.sum([w*x for w,x in zip(self.w,row)])+self.b for row in X]
        return predictions
    def calculate_cost(self,predictions,y):
        sums = [(predictions[i]-y[i])**2 for i in range(len(y))]
        cost = sum(sums)/len(y)
        return cost
    def apply_gradient_descent(self):
        for i in range(100):
            error = np.array(self.predictions).reshape(-1,1)-self.y_train.reshape(-1,1)
            w_grad =(np.dot(error.T,self.X_train))/len(self.X_train)
            self.w -= self.lr*w_grad.flatten()
            b_grad = np.sum(error)/len(self.X_train)
            self.b -= self.lr*b_grad
            self.predictions =self.predict(self.X_train)
            self.cost = self.calculate_cost(self.predictions,self.y_train)
            print("iteration : ",i,"-----------------------------------------------------------------------")
            print("w",self.w)
            print("b",self.b)
            print("c",self.cost)
    def fit(self):
        self.predictions =self.predict(self.X_train)
        self.cost = self.calculate_cost(self.predictions,self.y_train)
        print("before :",self.cost)
        self.predictions =self.apply_gradient_descent()
        print("after: ",self.cost)

    def load_model(self,file_path):
          with open(file_path, "rb") as file_ref:
                lin_model = pickle.load(file_ref)  
          return lin_model    
    

