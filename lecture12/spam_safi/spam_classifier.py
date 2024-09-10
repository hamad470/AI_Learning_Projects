import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')

class SpamClassifier:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.model = None

    def preprocess_text(self, text):
        """Preprocess the input text by tokenizing, removing stopwords, and stemming."""
        text = text.lower()
        words = nltk.word_tokenize(text)
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        words = [self.stemmer.stem(word) for word in words]
        return ' '.join(words)

    def train_model(self, data_path='spam.csv'):
        """Train a decision tree model on the provided dataset."""
        df = pd.read_csv(data_path, encoding='ISO-8859-1')
        df = df.rename(columns={'v1': 'target', 'v2': 'text'})
        df['processed_text'] = df['text'].apply(self.preprocess_text)

        X = df['processed_text']
        y = df['target'].map({'ham': 0, 'spam': 1})

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', DecisionTreeClassifier(random_state=42))
        ])

        self.model.fit(X_train, y_train)
        joblib.dump(self.model, 'model.pkl')
        print("Model trained and saved as 'model.pkl'.")

    def load_model(self, model_path='model.pkl'):
        """Load a pre-trained model from a file."""
        self.model = joblib.load(model_path)
        print("Model loaded from 'model.pkl'.")

    def predict(self, message):
        """Predict whether the input message is spam or not."""
        if not self.model:
            raise Exception("Model is not loaded or trained.")
        cleaned_message = self.preprocess_text(message)
        prediction = self.model.predict([cleaned_message])[0]
        return "Spam" if prediction == 1 else "Not Spam"
