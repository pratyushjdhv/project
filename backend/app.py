from flask_security import utils
from argon2 import hash_password
from flask import Flask
from flask_restful import Api
from model import db
from flask_security import Security
from flask_cors import CORS

from config import Config
from user_datastore import datastore

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Security(app, datastore)

    api = Api(app)

    return app,api


def initiate_db(app):
    with app.app_context():
        db.create_all()

        admin_role = datastore.find_or_create_role(name="admin")
        manager_role = datastore.find_or_create_role(name="manager")
        instructor_role = datastore.find_or_create_role(name="instructor")
        student_role = datastore.find_or_create_role(name="student")

        if not datastore.find_user(username="admin"):
            datastore.create_user(
                username="admin",
                email="admin@example.com",
                password= utils.hash_password("admin123"),
                roles=[admin_role, student_role, manager_role, instructor_role],
            )
            print("admin created!!!")

        if not datastore.find_user(username="manager"):
            datastore.create_user(
                username="manager",
                email="manager@example.com",
                password= utils.hash_password("manager123"),
                roles=[manager_role],
            )
            print("manager created!!!")

        if not datastore.find_user(username="instructor"):
            datastore.create_user(
                username="instructor",
                email="instructor@example.com",
                password= utils.hash_password("instructor123"),
                roles=[instructor_role],
            )
            print("instructor created!!!")

        if not datastore.find_user(username="student"):
            datastore.create_user(
                username="student",
                email="student@example.com",
                password= utils.hash_password("student123"),
                roles=[student_role],
            )
            print("student created!!!")

        db.session.commit()
        print("Database created and users added.")

app, api = create_app()


CORS(app)

# from route import *

from apis.auth import LoginUser, LogoutUser, SignupUser
from apis.crud import Addmanager, Subs, Addinstructor, Addstud

# -------------------------------------------------------------------
# APIS

api.add_resource(LoginUser, '/login-user')
api.add_resource(LogoutUser, '/logout-user')
api.add_resource(SignupUser, '/signup-user')

# -----------------------------------------------------------------------------

api.add_resource(Subs, '/subjects', '/subjects/<string:sub_id>')
api.add_resource(Addinstructor, '/add-instructor/<string:user_id>')
api.add_resource(Addstud, '/add-student/<string:user_id>')
api.add_resource(Addmanager, '/add-manager/<string:user_id>')


if __name__ == "__main__":
    initiate_db(app)
    app.run(debug=True)
