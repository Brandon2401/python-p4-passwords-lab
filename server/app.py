#!/usr/bin/env python3

from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from config import db
from models import User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# -------------------------
# Routes
# -------------------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id

    return jsonify(user.to_dict()), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 200

    return jsonify({}), 401


@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop('user_id', None)
    return jsonify({}), 204


@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify(user.to_dict()), 200
    return jsonify({}), 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
