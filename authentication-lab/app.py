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
"databaseURL" : "https://banana-af64f-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(dictionary)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for("add_tweet"))
        except:
            error = "oppsie smol mistake try agean"
            return render_template("signin.html")
    else:
        return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email" : email, 'password': password, "full_name" : full_name, "username" : username, "bio" : bio}
            db.child("Users").child(UID).set(user)
            return redirect(url_for("add_tweet"))
        except:
            error = "oppsie smol mistake try agean"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            uid = login_session['user']['localId']
            tweet = {"title":title,"text":text, "uid":uid}
            db.child("Tweets").push(tweet)
        except:
            error = "failed/error"
    return render_template("add_tweet.html")


@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    auth.user = None
    login_session['user'] = None
    return render_template('signin.html')

@app.route('/all_tweets', methods = ['GET', 'POST'])
def all_tweets():
    tweets = db.child('Tweets').get().val()
    return render_template('tweets.html', tweets = tweets)

if __name__ == '__main__':
    app.run(debug=True)