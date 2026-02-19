from flask_restful import Resource
from flask import make_response, request, jsonify
from user_datastore import datastore
from flask_security import utils, auth_token_required
from model import db


class LoginUser(Resource):

    def post(self):

        login_creds = request.get_json()

        if (
            not login_creds
            or not login_creds.get("username")
            or not login_creds.get("password")
        ):
            val = {"message": "Invalid login credentials"}
            return make_response(jsonify(val), 400)

        username = login_creds["username"]
        password = login_creds["password"]

        user = datastore.find_user(username=username)
        if not user:
            return make_response(jsonify({"message": "Invalid username"}), 401)

        if not utils.verify_password(password, user.password):
            return make_response(jsonify({"message": "Invalid password"}), 401)

        auth_token = user.get_auth_token()

        utils.login_user(user)

        res = {
            "message": "Login successful",
            "auth_token": auth_token,
            "user": {
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles],
            },
        }

        return make_response(jsonify(res), 200)


class LogoutUser(Resource):

    @auth_token_required
    def post(self):
        utils.logout_user()

        result = {"message": "Logged out successfully"}
        return make_response(jsonify(result), 200)


# --------------------------------------------------------------------

class SignupUser(Resource):

    def post(self):

        user_creds = request.get_json()

        if (
            not user_creds
            or not user_creds.get("username")
            or not user_creds.get("email")
            or not user_creds.get("password")
        ):
            return make_response(
                jsonify(
                    {"message": "Missing required fields: username, email, password"}
                ),
                400,
            )

        username = user_creds["username"]
        email = user_creds["email"]
        password = user_creds["password"]

        if datastore.find_user(username=username):
            return make_response(jsonify({"message": "Username already exists"}), 400)

        if datastore.find_user(email=email):
            return make_response(jsonify({"message": "Email already exists"}), 400)
        
        if len(password) < 6:
            return make_response(jsonify({"message": "Password must be at least 6 characters long"}), 400)

        new_user = datastore.create_user(
            username=username,
            email=email,
            password=utils.hash_password(password),
        )

        db.session.add(new_user)
        db.session.commit()

        result = {
            "message": "User created successfully",
            "user": {
                "username": new_user.username,
                "email": new_user.email,
                "roles": [role.name for role in new_user.roles],
            },
        }

        return make_response(jsonify(result), 201)
