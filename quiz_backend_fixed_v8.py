import os
from concrete.ml.sklearn import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)

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

sentiment_model, vectorizer = train_sentiment_model()

@app.route('/api/quiz', methods=['POST'])
def process_quiz():
    data = request.json
    a = float(data['a'])
    b = float(data['b'])
    user_answer = float(data['user_answer'])
    explanation = data.get('explanation', '')
    correct = abs((a + b) - user_answer) < 1e-6
    X_text = vectorizer.transform([explanation]).toarray()
    sentiment_prob = sentiment_model.predict_proba(X_text, fhe="execute")[0][1]
    sentiment_label = "POSITIVE" if sentiment_prob > 0.5 else "NEGATIVE"
    feedback = f"You {'nailed it!' if correct else 'Keep trying!'} Sentiment: {sentiment_label}"
    result = {
        "score": int(correct),
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
