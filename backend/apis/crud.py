from flask_restful import Resource
from flask import make_response, request, jsonify
from user_datastore import datastore
from flask_security import utils, auth_token_required, roles_required
from model import Subjects, db


class Subs(Resource):
    # /subjects
    def get(self):

        subjects = db.session.query(Subjects).all()

        if not subjects:
            return make_response(jsonify({"error": "No subjects found"}), 404)

        result = []
        for subject in subjects:
            result.append(
                {
                    "id": subject.id,
                    "sub_id": subject.sub_id,
                    "name": subject.name,
                    "description": subject.description,
                }
            )
        return make_response(jsonify(result), 200)

    # /subjects/<string: sub_id>
    def get(self, sub_id):

        subject = Subjects.query.get(sub_id)

        if not subject:
            return make_response(jsonify({"error": "Subject not found"}), 404)

        result = {
            "message": "Subject retrieved successfully",
            "details": {
                "id": subject.id,
                "sub_id": subject.sub_id,
                "name": subject.name,
                "description": subject.description,
            },
        }

        return make_response(jsonify(result), 200)

    def post(self):
        data = request.get_json()

        sub_id = data.get("sub_id")
        name = data.get("name")
        description = data.get("description")

        if not sub_id or not name:
            return make_response(
                jsonify({"error": "sub_id and name are required"}), 400
            )

        sub = Subjects.query.filter_by(sub_id=sub_id).first()
        if sub:
            return make_response(
                jsonify({"error": "Subject with this sub_id already exists"}), 409
            )

        new_subject = Subjects(sub_id=sub_id, name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()

        result = {
            "message": "Subject added successfully",
            "details": {
                "id": new_subject.id,
                "sub_id": new_subject.sub_id,
                "name": new_subject.name,
                "description": new_subject.description,
            },
        }

        return make_response(jsonify(result), 201)

    def delete(self, sub_id):
        subject = Subjects.query.get(sub_id)
        if not subject:
            return make_response(jsonify({"error": "Subject not found"}), 404)

        db.session.delete(subject)
        db.session.commit()

        result = {
            "message": "Subject deleted successfully",
        }

        return make_response(jsonify(result), 200)


# ---------------------------------------------------------------------------------


class Addinstructor(Resource):
    @auth_token_required
    @roles_required(["admin", "manager"])

    def patch(self, user_id):

        input = request.get_json()

        user = datastore.find_user(id=user_id)

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        role = "instructor"

        if not datastore.find_role(role):
            return make_response(jsonify({"message": "Role not found"}), 404)

        user.roles.append(datastore.find_role(role))
        db.session.commit()

        result = {
            "message": "User updated successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles],
            },
        }

        return make_response(jsonify(result), 200)


class Addstud(Resource):
    @auth_token_required
    @roles_required(["admin", "manager"])
    def patch(self, user_id):

        input = request.get_json()

        user = datastore.find_user(id=user_id)

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        role = "student"
        
        if not datastore.find_role(role):
            return make_response(jsonify({"message": "Role not found"}), 404)

        user.roles.append(datastore.find_role(role))
        db.session.commit()

        result = {
            "message": "User updated successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles],
            },
        }

        return make_response(jsonify(result), 200)
    
class Addmanager(Resource):
    @auth_token_required
    @roles_required(["admin"])

    def patch(self, user_id):

        input = request.get_json()

        user = datastore.find_user(id=user_id)

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        role = "manager"

        if not datastore.find_role(role):
            return make_response(jsonify({"message": "Role not found"}), 404)

        user.roles.append(datastore.find_role(role))
        db.session.commit()

        result = {
            "message": "User updated successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles],
            },
        }

        return make_response(jsonify(result), 200)
    
# ----------------------------------------------------------------------------------------
