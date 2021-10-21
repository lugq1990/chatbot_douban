
from flask import Flask, render_template, redirect, url_for, request, Blueprint
import os

from database import User, UserDatabase


app = Flask(__name__)
auth = Blueprint('auth', __name__)

user_database = UserDatabase()

@app.route('/')
def index():
    return "This is home page"

#todo: after we have already get data from frontend, if signup then dump data into DB with timestamp, otherwise should first check!
# todo2: add flask session manager to get keep session.


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get("username")
    password = request.form.get("password")

    # todo: How to return back with some error msg?
    print("Get username:", username)
    exist, msg = user_database.check_user(username=username, password=password)
    if not exist:
        print(msg)
        return render_template('login.html')
    else:
        return render_template("profile.html")
        


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get("password")

        user = User(username=username, email=email, password=password)
        
        if not username or not email or not password:
            print("Not get satisy data!")
            return redirect(url_for('signup'))
        else:
            
            user_database.insert(user_obj=user)
            return redirect(url_for('login'))
        
    

if __name__ == '__main__':
    app.run(debug=True)