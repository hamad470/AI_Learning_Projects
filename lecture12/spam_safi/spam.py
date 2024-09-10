from flask import Flask, render_template, request
from spam_classifier import SpamClassifier

# Initialize Flask app
app = Flask(__name__)

# Initialize and load the SpamClassifier
classifier = SpamClassifier()
classifier.load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        prediction = classifier.predict(message)
        return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
