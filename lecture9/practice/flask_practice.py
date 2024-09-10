from flask import Flask, request, render_template,jsonify
import numpy as np
import pandas as pd
import numpy as np
from flask_cors import CORS
from Controller import Prediction_controller
from bitcoin import CustomLinearRegression
app = Flask(__name__)
CORS(app)
obj_controller = Prediction_controller()

# Unix timestamp





# Convert timestamp to datetime


import pandas as pd

@app.route('/about_us')
def about():
     return render_template('about.html')
@app.route('/prediction')
def prediction():
     return render_template('prediction.html')
@app.route('/previous_data')
def show_previous_data():
    page_data,page,total_pages,start_page,end_page,df=obj_controller.pagination(request)
    return render_template(
        'previous_data.html',
        data=page_data,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        g_data =obj_controller.df
    )



@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")
@app.route("/subscribe", methods=["POST"])
def subscribe():
    message =obj_controller.subscribe()
    return jsonify({"message":message})
@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")
@app.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template("signin.html")
@app.route("/signin_validation", methods=["POST"])
def validate_sigin():
     message = obj_controller.validate_sigin(request)
     return jsonify({"message":message})
     

@app.route("/register", methods=["POST"])
def register():
     message = obj_controller.register(request)
     return jsonify({"message":message})
@app.route('/data',methods=['POST'])

def submit_data():
        
        if request.method == "POST":
            X_p_inp=obj_controller.receive_and_process_data(request)
            prediction = obj_controller.predict(X_p_inp)
            return jsonify({"message":prediction})
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port = 5000)
