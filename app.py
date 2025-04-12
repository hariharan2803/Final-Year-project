from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, url_for, flash, session
from textblob import TextBlob
from collections import Counter
import mysql.connector
import os
from flask import Flask
import re 
from app2 import app2 
app = Flask(__name__)

app.register_blueprint(app2, url_prefix='/app2')

# Initialize Flask app

app.secret_key = os.urandom(24)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    port = 3307,
    user="root",
    password="harir2803",
    database="mental_health_db"
)

cursor = db.cursor(dictionary=True)  
@app.route('/')
def index():
    if 'username' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))  
    return render_template('index.html', username=session['username'])

@app.route('/start_app2')
def start_app2():
    return redirect(url_for('app2.new_index'))

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template('quiz.html')

@app.route('/quiz1')
def quiz1():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template('quiz1.html')

@app.route('/quiz2')
def quiz2():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template('quiz2.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'username' not in session:
        return redirect(url_for('signup'))

    quiz_type = request.form.get('quiz_type')
    responses = {key: request.form.getlist(key)[0] if len(request.form.getlist(key)) == 1 else request.form.getlist(key)
                 for key in request.form}  # Handles lists properly
    
    print(f"Received responses: {responses}")

    negative_responses = {
        "rarely", "frequently", "almost always", "slightly dissatisfied",
        "not satisfied", "needs improvement", "poor", "monthly",
        "not very confident", "not confident at all", "often",
        "almost every day", "significantly", "unable to manage",
        "lack of focus", "feeling exhausted", "overwhelmed",
        "disorganized", "low energy", "burnout", "anxious",
        "somewhat worse", "it’s challenging but manageable",
        "a few times a month", "i feel isolated", "almost every night",
        "very stressed", "struggling to adapt", "frequently, and it’s concerning",
        "no, not at all", "frequently overwhelmed"
    }

    stress_count = 0
    response_options = []
    total_questions = len(responses) - 1  # Excluding 'quiz_type'

    for key, value in responses.items():
        if key == 'quiz_type':
            continue

        # Ensure value is a string before processing
        if isinstance(value, list):
            value = value[0]  # Take the first answer if multiple exist

        cleaned_value = re.sub(r"[^\w\s']", "", value.lower().strip())  # Keep apostrophes for proper sentiment analysis

        # Debugging print
        print(f"Processing Key: {key}, Original Value: '{value}', Cleaned Value: '{cleaned_value}'")

    

        # Exact word match instead of partial 'in' checks
        if any(re.search(rf"\b{re.escape(neg_word)}\b", cleaned_value) for neg_word in negative_responses):
            stress_count += 1
        else:
            sentiment = TextBlob(value).sentiment.polarity
            if sentiment < -0.2:  
                stress_count += 1

    counts = Counter(response_options)

    threshold = 5 if total_questions == 12 else 4 # Adjust threshold based on total questions
    high_stress_count = counts.get(3, 0) + counts.get(4, 0) + stress_count

    # Debugging print
    print(f"Quiz Type: {quiz_type}, Total Questions: {total_questions}, Threshold: {threshold}, High Stress Count: {high_stress_count}")
    print(f"Response Options Count: {counts}")
    print(f"Text-Based Stress Count: {stress_count}")

    # Redirect based on stress level
    if high_stress_count >= threshold:  
        session['stress_level'] = "High Stress"
        print("Redirecting to Rejuvenation")
        return redirect(url_for('rejuvenation'))

    session['stress_level'] = "Low to Medium Stress"
    print("Redirecting to Positive Recommendations")
    return redirect(url_for('positive_recommendations'))

@app.route('/positive_recommendations')
def positive_recommendations():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template('positive_recommendations.html')

@app.route('/rejuvenation')
def rejuvenation():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template('rejuvenation.html')

@app.route('/stress_report')
def stress_report():
    if 'username' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    username = session['username']
    stress_level = session.get('stress_level', 'Unknown')  # Get stress level from session

    # Determine recommendation message
    if stress_level == "High Stress":
        recommended_page = "Rejuvenation"
        message = f"Hi {username}, your stress level is high. You are recommended to improve your stress level positively. Please visit our recommended page and make use of it 😊"
    else:
        recommended_page = "Positive Recommendations"
        message = f"Hi {username}, your stress level is low to medium. You are recommended to manage your stress level positively. Please visit our recommended page and make use of it 😊"

    return render_template('report.html', user_name=username, stress_level=stress_level, message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('signup'))

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username or Email already exists. Please choose a different one.', 'warning')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)  # Secure password hashing
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        db.commit()

        flash('Sign-up successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and Password are required!', 'danger')
            return redirect(url_for('login'))

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):  
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid login details. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('signup'))

if __name__ == '__main__':
    app.run(debug=True)

