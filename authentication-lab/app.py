from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyrebase
from datetime import datetime


CONFIG = {
  "apiKey" : "AIzaSyBfR-dCykhSpaRhiOCjpyXaVcQxygSkFJ4",
  "authDomain" : "auth-lab-65e0e.firebaseapp.com",
  "projectId" : "auth-lab-65e0e",
  "storageBucket" : "auth-lab-65e0e.appspot.com",
  "messagingSenderId" : "485834454591",
  "appId" : "1:485834454591:web:8536a1e052b58c85a5ea8a",
  "measurementId" : "G-TR8P602N4W",
  "databaseURL" : "https://auth-lab-65e0e-default-rtdb.europe-west1.firebasedatabase.app"
  }

firebase = pyrebase.initialize_app(CONFIG)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect(url_for('add_tweet'))
        except:
            flash('Invalid Credentials')
            return redirect(url_for('signin'))
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        fullname = request.form['fullname']
        password = request.form['password']
        session['username'] = request.form['username']
        try:
            session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {'name': fullname, 'email': email}
            db.child("Users").child(session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except Exception:
            flash('Email already in use')
            return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet = { 'tweetBody': request.form['body'], 'Title': request.form['title'], 'Author': session['username'], 'currentTime': datetime.now().strftime("%H:%M:%S") }
        try:
            db.child("Users").child(session['user']['localId']).child("Tweets").push(tweet) # push to the database
            return redirect(url_for('tweets'))
        except Exception:
            flash('Error adding tweet')
            return redirect(url_for('add_tweet'))
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET', 'POST'])
def tweets():
    return render_template("all_tweets.html", tweets=db.child("Users").child(session['user']['localId']).child("Tweets").get().val().values())


@app.route('/logout', methods=['GET', 'POST'])
def logout(logout):
    if logout:
        session['User'] = None
        auth.current_user = None
    return render_template("logout.html")


if __name__ == '__main__':
    app.run(debug=True)