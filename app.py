from flask import Flask, request, render_template, redirect, url_for, flash, session
from textblob import TextBlob
from collections import Counter

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages and session handling

# Dummy user storage (replace with actual database in production)
users = {}

@app.route('/')
def index():
    
    if 'username' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))  

    return render_template('index.html', username=session['username'])


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
    responses = [
        request.form.get('academicStress'),
        request.form.get('workLifeBalance'),
        request.form.get('concentrationDifficulty'),
        request.form.get('sleepHours'),
        request.form.get('physicalActivity'),
        request.form.get('socialLife'),
        request.form.get('futureAnxiety'),
        request.form.get('pressureHandling'),
        request.form.get('breaks'),
        request.form.get('financialSatisfaction')
    ]
    response_options = [int(option) for option in responses if option and option.isdigit()]
    counts = Counter(response_options)

    print(f"Quiz submission responses: {responses}")  # Debugging line to check the responses
    print(f"Counter result: {counts}")  # Debugging line to check the counts of responses

    if counts.get(1, 0) + counts.get(2, 0) > 6:
        return redirect(url_for('positive_recommendations'))
    elif counts.get(3, 0) + counts.get(4, 0) > 6:
        return redirect(url_for('rejuvenation'))

    return redirect(url_for('rejuvenation'))

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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Basic validation for empty fields
        if username == '' or password == '':
            flash('Username and Password are required!', 'danger')
            return redirect(url_for('signup'))
        
        # Check if user already exists
        if username in users:
            flash('Username already exists. Please choose a different one.', 'warning')
            return redirect(url_for('signup'))
        
        # Register the user
        users[username] = password
        session['username'] = username  # Set the session variable for the logged-in user
        flash('Sign-up successful! Please log in.', 'success')
        return redirect(url_for('login'))  

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Basic validation for empty fields
        if username == '' or password == '':
            flash('Username and Password are required!', 'danger')
            return redirect(url_for('login'))

        # Check if user exists and password matches
        if username in users and users[username] == password:
            session['username'] = username  # Store the logged-in user's session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the main page after successful login
        else:
            flash('Invalid login details. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash("You have been logged out.")
    return redirect(url_for('signup'))

if __name__ == '__main__':
    app.run(debug=True)



