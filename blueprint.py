from flask import Blueprint, jsonify, request
from schemes import UserSchema
from models import Session, User
from marshmallow import ValidationError


api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.route('/user', methods=['POST'])
def create_user():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    try:
        user_data = UserSchema().load(data)
    except ValidationError as err:
        return err.messages, 422

    the_user = User(**user_data)
    # print(the_user)

    user_find = session.query(User).filter_by(name=data['name']).first()
    if user_find:
        # print(user_find)
        return {"message": "User with such username already exists"}, 400

    user_find = session.query(User).filter_by(email=data['email']).first()
    if user_find:
        # print(user_find)
        return {"message": "User with such email already exists"}, 400

    session.add(the_user)
    session.commit()

    result = UserSchema().dump(the_user)
    return jsonify(result)
