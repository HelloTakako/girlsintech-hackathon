from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from helpers import database, forms
from werkzeug.utils import secure_filename
import hashlib
import json
import os


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './data'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



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
    return render_template('map.html',challenge =   {
    "Title": "Introduction",
    "Content": "Blablabla"
  })


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
def challenges(day, picture = None):
    with open('data/challenges.json') as file:
        challenges = json.load(file)
    try:
        challenge = challenges[day - 1]

    except IndexError:
        challenge = {
    "Title": "Work in progress",
    "Content": "No challenge defined for today"
  }
    return render_template('map.html',challenge = challenge, picture = picture)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/uploads/<int:challenge_id>', methods=['GET','POST'])
def upload_file(challenge_id):
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            print('foo')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('map',challenge = challenge_id,
                                    picture=filename))








if __name__ == '__main__':
    app.run()
