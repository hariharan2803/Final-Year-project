import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template, send_file, Blueprint, redirect, url_for
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO

app2 = Blueprint('app2', __name__) 



# Load pre-trained model and vectorizer
with open('models/stress_detection_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to predict stress levels
def get_combined_stress_level(text):
    # VADER prediction
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    vader_stress = 3 if compound_score <= -0.5 else \
                   2 if -0.5 < compound_score <= -0.2 else \
                   1 if -0.2 < compound_score <= 0.2 else 0

    # Model prediction
    text_vec = vectorizer.transform([text])
    model_prediction = model.predict(text_vec)[0]
    model_stress = 3 if model_prediction == "High Stress" else \
                   2 if model_prediction == "Medium Stress" else \
                   1 if model_prediction == "Low Stress" else 0

    # Combine predictions
    avg_stress = (vader_stress + model_stress) / 2
    if avg_stress >= 2.5:
        return "High Stress"
    elif avg_stress >= 1.5:
        return "Medium Stress"
    elif avg_stress >= 0.5:
        return "Low Stress"
    else:
        return "Neutral"

# Store inputs and results for visualization
inputs = []
stress_levels = []

@app2.route('/')
def index():
   return redirect(url_for('app2.new_index'))

@app2.route('/new_index')  
def new_index():
    return render_template('new_index.html')

@app2.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_text = data['text']

    # Get stress level
    stress_level = get_combined_stress_level(user_text)
    inputs.append(user_text)
    stress_levels.append(stress_level)

    return jsonify({'stress_level': stress_level})

@app2.route('/visualize', methods=['GET'])
def visualize():
    # Map stress levels to numeric values
    stress_numeric = [3 if level == "High Stress" else 
                      2 if level == "Medium Stress" else 
                      1 if level == "Low Stress" else 0 for level in stress_levels]

    # Plot the stress trend
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(stress_levels)), stress_numeric, marker='o', linestyle='-', color='purple')
    plt.title("Stress Level Trend Over Time")
    plt.xlabel("Input Sequence")
    plt.ylabel("Stress Level (0: Neutral, 1: Low, 2: Medium, 3: High)")
    plt.xticks(range(len(stress_levels)), labels=range(1, len(stress_levels) + 1))
    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


