#!/usr/bin/env python3
'''flask app'''
from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_flask():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.register_user(email=email, password=password)
        response_data = {"email": email, "message": "user created"}
        return jsonify(response_data), 200
    except ValueError as e:
        response_data = {"message": str(e)}
        return jsonify(response_data), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)
    if not valid_user:
        abort(401)

    session_id = AUTH.create_session(email=email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
