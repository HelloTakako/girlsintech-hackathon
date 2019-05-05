from flask import Flask, render_template, redirect, url_for, request, flash
from helpers import database, forms
from flask_login import current_user, login_user, logout_user, LoginManager
import hashlib
import json


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        user = None

        for existing_user in database.users:
            if existing_user['email'] == request.form['email']:
                user = existing_user

        password = hashlib.sha3_256(request.form['password'].encode('utf-8')).hexdigest()

        if user:
            if user['password_hash'] == password:
                user['is_logged'] = True
                flash('You are now logged in', 'success')
                return redirect(url_for('map'))

            else:
                user['is_logged'] = False
                flash('Invalid credentials','Warning')

        else:
            flash('Unknown email','Warning')

    return render_template('login.html')


@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.Registerform(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = database.User(username,password,email)

        user.create()

        return render_template('map.html', form=form)

    return render_template('login.html', form=form)


@app.route('/day/<int:day>')
def challenges(day):
    with open('data/challenges.json') as file:
        challenges = json.load(file)
    print(challenges[day])

    return render_template('map.html',challenge = challenges[day])



if __name__ == '__main__':
    app.run()
