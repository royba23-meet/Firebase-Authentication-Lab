from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyrebase

CONFIG = {
  "apiKey" : "AIzaSyBfR-dCykhSpaRhiOCjpyXaVcQxygSkFJ4",
  "authDomain" : "auth-lab-65e0e.firebaseapp.com",
  "projectId" : "auth-lab-65e0e",
  "storageBucket" : "auth-lab-65e0e.appspot.com",
  "messagingSenderId" : "485834454591",
  "appId" : "1:485834454591:web:8536a1e052b58c85a5ea8a",
  "measurementId" : "G-TR8P602N4W",
  "databaseURL" : ""
  }

firebase = pyrebase.initialize_app(CONFIG)
auth = firebase.auth()


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
        password = request.form['password']
        try:
            session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except Exception:
            flash('Email already in use')
            return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


@app.route('logout', methods=['GET', 'POST'])
def logout(logout):
    if logout:
        session['User'] = None
        auth.current_user = None
    return render_template("logout.html")


if __name__ == '__main__':
    app.run(debug=True)