# main.py

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from database import Database
import authentication
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

# TODO: This is causing issues with other routes
@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        json_data = request.form
        email = json_data.get('email')
        password = json_data.get('password')

        # Insert user into database
        status = authentication.create_new_user(email, password)

        return jsonify({'result': status})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        json_data = request.form
        email = json_data.get('email')
        password = json_data.get('password')
        status = authentication.login(email, password)
        if status:
            session['logged_in'] = True
            session['user'] = email
            return redirect(url_for('main'))
        else:
            # TODO: Give message that login was incorrect
            return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
