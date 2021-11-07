from flask import jsonify, request
from schemes import UserSchema
from models import Session, User
from marshmallow import ValidationError
from flask import Blueprint
from flask_bcrypt import Bcrypt


api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.route('/user', methods=['POST'])
def create_user():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    if data['password']:
        data['password'] = Bcrypt().generate_password_hash(data['password']).decode('utf - 8')
    else:
        # check code + message change
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


@api_blueprint.route('/user/login', methods=['GET'])
def login_user():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    user_find = session.query(User).filter_by(name=data['name']).first()
    if not user_find:
        # print(user_find)
        return {"message": "User with such username does not exists"}, 401

    if data['password'] != user_find.password:
        return {"message": "Provided credentials are invalid"}, 401

    result = UserSchema().dump(user_find)
    return jsonify(result)
