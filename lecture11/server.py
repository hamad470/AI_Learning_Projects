from flask import Flask, request, render_template, redirect, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.preprocessing import StandardScaler
from controller.controller_prediction import PredictionController
app = Flask(__name__)
CORS(app)

# Hardcoded user database
database = {'safi': '123', 'james': 'aac', 'akhlaq': 'asdsf'}

@app.route('/')
def hello_world():
    return render_template("predictions.html")

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    controller = PredictionController(request)
    response = controller.login(name, email, password)
    return render_template("login.html", context={'response': response})

@app.route('/signup', methods=['POST'])
def sign_up():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    controller = PredictionController(request)
    response = controller.sign_up(name, email, password)
    return render_template("signup.html", context={'response': response})


@app.route('/find_data_daily', methods=['POST'])
def find_data_daily():
    if request.method == 'POST':
        # Accessing json data from request
        data = request.get_json()
        w = [0.24968935, 0.24705427, 0.24762563, 0.24762563, 0.01461352]
        b =  [-0.01576464]
        
        # Extract and prepare the input data
        x = np.array([
            (float(data.get('open'))-1.741912e+04)/1.929588e+04,
            (float(data.get('low'))-1.699393e+04)/1.881681e+04,
            (float(data.get('close'))-1.743467e+04)/1.930544e+04,
            (float(data.get('adj'))-1.743467e+04)/1.930544e+04,
            (float(data.get('vol'))-1.751004e+10)/1.921570e+10
            ]).reshape(1, -1)

        # Standardize x
        print(x)
        
        # Linear combination with standardized inputs
        y_standardized = np.dot(x, w) + b

        # Manually reverse the standardization for the prediction
        y_original = y_standardized * 1.973042e+04 + 1.781639e+04
        
        # Convert the NumPy array to a Python float
        y_original = y_original.item()

        context = {'message': y_original}  # Prepare the response
        return jsonify(context)
    else:
        return "POST DATA"



if __name__ == '__main__':
    app.run(debug=True)
