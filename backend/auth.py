from flask_restful import Resource
from flask import make_response, request, jsonify
from user_datastore import datastore
from flask_security import utils, auth_token_required


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

        result = {
            "message" : "Logged out successfully"
        }
        return make_response(jsonify(result), 200)
