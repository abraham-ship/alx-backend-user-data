#!/usr/bin/env python3
'''flask app'''
from flask import Flask
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    user_request = request.form
    user_email = user_request.get('email')
    is_registered = AUTH.create_session(user_email)

    if not is_registered:
        abort(403)
    token = AUTH.get_reset_password_token(user_email)
    message = {"email": user_email, "reset_token": token}
    return jsonify(message)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    user_email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        message = {"email": user_email, "message": "Password updaed"}
        return jsonify(message), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
