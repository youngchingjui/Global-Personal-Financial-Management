# main.py

from flask import Flask, request, jsonify, render_template, session
from database import Database
import authentication
import bcrypt

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

# TODO: This is causing issues with other routes
@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.methods == 'GET':
        return render_template('register.html')
    elif request.methods == 'POST':
        json_data = request.json
        email = json_data['email'],
        password = json_data['password']

        # Insert user into database
        status = authentication.create_new_user(email, password)

        return jsonify({'result': status})

@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    email = json_data['email'],
    password = json_data['password']

    status = authentication.login(email, password)
    if status:
        session['logged_in'] = True

    return jsonify({'result': status})

if __name__ == '__main__':
    app.run(debug=False)
