from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

dictionary =  {
"apiKey": "AIzaSyBP8jkjzHxGltZn7_IMUbFAtGeeWjbpvR4",
  "authDomain": "banana-af64f.firebaseapp.com",
  "projectId": "banana-af64f",
  'storageBucket': "banana-af64f.appspot.com",
  'messagingSenderId': "866519119331",
  'appId': "1:866519119331:web:a0ed17b1abffe163dadcd6",
  'measurementId': "G-2XGQD7LMFK",
"databaseURL" : ""
}

firebase = pyrebase.initialize_app(dictionary)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return render_template("add_tweet.html")
        except:
            error = "oppsie smol mistake try agean"
            return render_template("signin.html")
    else:
        return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    auth.user = None
    login_session['user'] = None
    return render_template('signin.html')



if __name__ == '__main__':
    app.run(debug=True)