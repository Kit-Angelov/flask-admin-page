from flask import Flask, request, jsonify, session, render_template, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import DB_CONFIG

app = Flask(__name__)
db_connect = "postgresql://{user}:{password}@{host}:{port}/{name}".format(**DB_CONFIG)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .models import *


def authorize(f):
    def wrapp(*args, **kws):
        user_id = session.get('user_id')
        if user_id is None:
            redirect(url_for('login'))
        user = User.query.get(user_id)
        return f(user, *args, **kws)
    return wrapp


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        response = Response(response='invalid login or password', status=401, mimetype="text/plane")

        if username is '' or password is '':
            return response
        user = User.login(username, password)
        if user is None:
            return response
        session['user_id'] = user.id
        return jsonify({'result': 'ok'})


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', ], endpoint='profile')
@authorize
def get_profile(user):
    response = {
        'username': user.username,
        'role': user.role.name,
        'id': user.id
    }
    return jsonify(response)


@app.route('/users', methods=['GET', ], endpoint='users')
@authorize
def get_users(user):
    response = list()
    users = User.query.all()
    for user in users:
        user_dict = {
            'username': user.username,
            'role': user.role.name,
            'role_id': user.role.id,
            'id': user.id
        }
        response.append(user_dict)
    return jsonify(response)


@app.route('/save_user', methods=['POST', ], endpoint='save_user')
@authorize
def save_user(user):
    if user.role.name != 'admin':
        response = Response(response='you are is not admin', status=403, mimetype="text/plane")
        return response
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    role_id = request.json.get('role_id', None)
    user_id = request.json.get('id', None)

    if User.query.filter_by(username=username).first() and user_id is None:
        response = Response(response='username already exist', status=500, mimetype="text/plane")
        return response
    
    if user_id:
        new_user = User.query.get(user_id)
        new_user.username = username
        new_user.role_id = role_id
        if password:
            new_user.set_password(password)
    else:
        new_user = User(username=username, role_id=role_id)
        new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'result': 'ok'})


@app.route('/delete_user', methods=['POST', ], endpoint='delete_user')
@authorize
def delete_user(user):
    if user.role.name != 'admin':
        response = Response(response='you are is not admin', status=403, mimetype="text/plane")
        return response
    deleted_user_id = request.json.get('user_id', None)
    deleted_user = User.query.get(deleted_user_id)
    db.session.delete(deleted_user)
    db.session.commit()
    return jsonify({'result': 'ok'})


@app.route('/get_roles', methods=['GET', ], endpoint='get_roles')
@authorize
def get_roles(user):
    roles = Role.query.all()
    response = list()
    for role in roles:
        item_role = {
            'name': role.name,
            'id': role.id
        }
        response.append(item_role)
    return jsonify(response)


@app.route("/", methods=['GET', ], endpoint='index')
@authorize
def index(user):
    return render_template('index.html')
