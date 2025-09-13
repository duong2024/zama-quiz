import os
from concrete.ml.sklearn import XGBClassifier, LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def train_quiz_model():
    X_train = np.array([
        [1.0, 2.0, 3.0], [4.0, 5.0, 9.0], [1.0, 1.0, 2.0], [3.0, 4.0, 7.0],
        [10.0, 20.0, 30.0], [5.0, 6.0, 11.0], [2.0, 3.0, 5.0], [8.0, 9.0, 17.0],
        [15.0, 25.0, 40.0], [7.0, 8.0, 15.0], [12.0, 13.0, 25.0], [6.0, 7.0, 13.0],
        [20.0, 30.0, 50.0], [9.0, 10.0, 19.0], [11.0, 12.0, 23.0], [14.0, 16.0, 30.0],
        [25.0, 35.0, 60.0], [18.0, 19.0, 37.0], [21.0, 22.0, 43.0], [13.0, 15.0, 28.0]
    ])
    y_train = np.array([1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])
    model = XGBClassifier(random_state=42)
    model.fit(X_train, y_train)
    model.compile(X_train)
    model.fhe_circuit.keygen()
    return model

def train_sentiment_model():
    texts = [
        "I'm happy because I got it right", "I'm sad because I got it wrong", "Super cool!",
        "Keep trying", "This is awesome!", "I feel bad about this", "Great job!",
        "Need to improve", "Fantastic result!", "Disappointing", "Well done!",
        "Not good enough", "Excellent!", "Upset with the outcome", "Proud of myself",
        "Frustrated", "Thrilled!", "Down in the dumps", "Over the moon!", "Bummed out"
    ]
    labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    vectorizer = TfidfVectorizer(max_features=50)
    X_train_text = vectorizer.fit_transform(texts).toarray()
    model = LogisticRegression(random_state=42)
    model.fit(X_train_text, labels)
    model.compile(X_train_text)
    model.fhe_circuit.keygen()
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    return model, vectorizer

quiz_model = train_quiz_model()
sentiment_model, vectorizer = train_sentiment_model()

@app.route('/api/quiz', methods=['POST'])
def process_quiz():
    data = request.json
    a = float(data['a'])
    b = float(data['b'])
    user_answer = float(data['user_answer'])
    explanation = data['explanation']
    features = np.array([[a, b, user_answer]])
    score = quiz_model.predict(features, fhe="execute")[0]
    explanation_plain = explanation
    X_text = vectorizer.transform([explanation_plain]).toarray()
    sentiment_prob = sentiment_model.predict_proba(X_text, fhe="execute")[0][1]
    sentiment_label = "POSITIVE" if sentiment_prob > 0.5 else "NEGATIVE"
    feedback = f"You {'nailed it! ??' if score == 1 else 'Keep trying! ??'} Sentiment: {sentiment_label}"
    result = {
        "score": int(score),
        "sentiment": sentiment_label,
        "feedback": feedback
    }
    return jsonify({"result": result})
@app.get("/")
def health():
    return "ok", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
