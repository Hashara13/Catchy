from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv() 
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

@app.route('/match', methods=['POST'])
def match_resume_job():
    data = request.json
    resume_text = preprocess(data['resume'])
    job_description = preprocess(data['job_description'])

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2]).flatten()[0]
    
    return jsonify({'similarity_score': similarity})

if __name__ == '__main__':
    app.run(debug=True)
