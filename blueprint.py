from flask import jsonify, request
from schemes import UserSchema, TagSchema, NoteSchema, NoteStatisticsSchema
from models import Session, User, Tag, Note, NoteStatistics
from marshmallow import ValidationError
from flask import Blueprint
from flask_bcrypt import Bcrypt
from datetime import datetime


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
        return {"message": "No password data provided"}, 400

    try:
        user_data = UserSchema().load(data)
    except ValidationError as err:
        return err.messages, 422

    the_user = User(**user_data)

    user_find = session.query(User).filter_by(name=data['name']).first()
    if user_find:
        return {"message": "User with such username already exists"}, 400

    user_find = session.query(User).filter_by(email=data['email']).first()
    if user_find:
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
        return {"message": "User with such username does not exists"}, 404

    if not Bcrypt().check_password_hash(user_find.password, data['password']):
        return {"message": "Provided credentials are invalid"}, 400

    result = UserSchema().dump(user_find)
    return jsonify(result)


@api_blueprint.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    user_find = session.query(User).filter_by(id=id).first()
    if not user_find:
        return {"message": "User with such id does not exists"}, 400

    # checking if suitable new username
    if 'name' in data:
        check_user = session.query(User).filter_by(name=data['name']).first()
    else:
        check_user = None
    if check_user:
        return {"message": "User with such username already exists"}, 400

    # checking if suitable new email
    if 'email' in data:
        check_user = session.query(User).filter_by(email=data['email']).first()
    else:
        check_user = None
    if check_user:
        return {"message": "User with such email already exists"}, 400

    # getting attributes of User class
    attributes = User.__dict__.keys()

    # updating
    for key, value in data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403

        if key not in attributes:
            return {"message": "Invalid input data provided"}, 400

        if key == 'password':
            value = Bcrypt().generate_password_hash(value).decode('utf - 8')

        setattr(user_find, key, value)

    # commit
    session.commit()

    user_find = session.query(User).filter_by(id=id).first()
    result = UserSchema().dump(user_find)

    return jsonify(result)


@api_blueprint.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    session = Session()

    user_find = session.query(User).filter_by(id=id).first()
    if not user_find:
        return {"message": "User with such id does not exists"}, 404

    result = UserSchema().dump(user_find)

    session.delete(user_find)
    session.commit()

    return jsonify(result)


@api_blueprint.route('/userstatistics/<int:id>', methods=['GET'])
def get_user_statistics(id):
    session = Session()

    statistics_find = session.query(NoteStatistics).filter_by(userId=id).all()
    if not statistics_find:
        return {"message": "You have no records done"}, 404

    result = []
    for stat in statistics_find:
        result.append(NoteStatisticsSchema().dump(stat))

    return jsonify(result)


@api_blueprint.route('/note', methods=['POST'])
def create_note():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    if 'idTag' not in data or 'idOwner' not in data:
        return {"message": "No input data provided"}, 400

    # checking name
    note_find = session.query(Note).filter_by(name=data['name']).first()
    if note_find:
        return {"message": "Note with such name already exists"}, 400

    # work with the tag
    tag_find = session.query(Tag).filter_by(name=data['idTag']).first()
    if tag_find:
        data['idTag'] = tag_find.id
    else:
        t_data = {'name': data['idTag']}
        tag_data = TagSchema().load(t_data)
        the_tag = Tag(**tag_data)
        session.add(the_tag)
        session.commit()

        tag_find = session.query(Tag).filter_by(name=data['idTag']).first()
        data['idTag'] = tag_find.id

    # checking the author
    user_find = session.query(User).filter_by(id=data['idOwner']).first()
    if not user_find:
        return {"message": "Provided credentials are invalid"}, 400

    try:
        note_data = NoteSchema().load(data)
    except ValidationError as err:
        return err.messages, 422

    the_note = Note(**note_data)
    session.add(the_note)
    session.commit()
    note_find = session.query(Note).filter_by(name=data['name']).first()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data_for_statistic = {'time': formatted_date, 'userId': data['idOwner'], 'noteId': note_find.id}

    try:
        statistic_data = NoteStatisticsSchema().load(data_for_statistic)
    except ValidationError as err:
        return err.messages, 422
    the_statistic = NoteStatistics(**statistic_data)
    session.add(the_statistic)
    session.commit()

    result = NoteSchema().dump(the_note)
    return jsonify(result)


@api_blueprint.route('/note/<int:id>', methods=['GET'])
def get_note(id):
    session = Session()

    note_find = session.query(Note).filter_by(id=id).first()
    if not note_find:
        return {"message": "Note with such id does not exists"}, 404

    result = NoteSchema().dump(note_find)
    return jsonify(result)


@api_blueprint.route('/note/<int:id>', methods=['PUT'])
def update_note(id):
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    note_find = session.query(Note).filter_by(id=id).first()
    if not note_find:
        return {"message": "Note with such id does not exists"}, 404

    # checking if suitable new name
    if 'name' in data:
        check_note = session.query(Note).filter_by(name=data['name']).first()
    else:
        check_note = None
    if check_note:
        return {"message": "Note with such username already exists"}, 400

    # getting attributes of Note class
    attributes = Note.__dict__.keys()

    # updating
    for key, value in data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403

        if key not in attributes:
            return {"message": "Invalid input data provided"}, 400

        if key == 'idOwner':
            return {"message": "You can not change idOwner"}, 403

        setattr(note_find, key, value)

    # commit
    session.commit()

    note_find = session.query(Note).filter_by(id=id).first()
    result = NoteSchema().dump(note_find)

    return jsonify(result)


@api_blueprint.route('/note/<int:id>', methods=['DELETE'])
def delete_note(id):
    session = Session()

    note_find = session.query(Note).filter_by(id=id).first()
    if not note_find:
        return {"message": "Note with such id does not exists"}, 404

    result = NoteSchema().dump(note_find)

    session.delete(note_find)
    session.commit()

    return jsonify(result)


@api_blueprint.route('/note_service', methods=['GET'])
def get_service():
    session = Session()

    find = session.query(Note).all()

    result = []
    for note in find:
        result.append(NoteSchema().dump(note))

    return jsonify(result)


@api_blueprint.route('/note_service/<int:id>', methods=['GET'])
def get_user_notes_by_id(id):
    session = Session()

    statistics_find = session.query(NoteStatistics).filter_by(userId=id).all()
    if not statistics_find:
        return {"message": "You have no records done"}, 404

    result = []
    for stat in statistics_find:
        note_find = session.query(Note).filter_by(id=stat.noteId).first()
        result.append(NoteSchema().dump(note_find))

    return jsonify(result)


@api_blueprint.route('/note_user', methods=['POST'])
def add_user_to_note():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    note_find = session.query(Note).filter_by(id=data['noteId']).first()
    if not note_find:
        return {"message": "Note with such id does not exists"}, 400

    user_find = session.query(User).filter_by(id=data['userId']).first()
    if not user_find:
        return {"message": "User with such username does not exists"}, 400

    statistics_find = session.query(NoteStatistics).filter_by(noteId=data['noteId']).all()
    if statistics_find:
        if len(statistics_find) > 5:
            return {"message": "Too many users are editing"}
        for stat in statistics_find:
            if int(data['userId']) == stat.userId:
                return {"message": "You already have the access"}

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data_for_statistic = {'time': formatted_date, 'userId': user_find.id, 'noteId': note_find.id}

    try:
        statistic_data = NoteStatisticsSchema().load(data_for_statistic)
    except ValidationError as err:
        return err.messages, 422
    the_statistic = NoteStatistics(**statistic_data)
    session.add(the_statistic)
    session.commit()

    result = NoteStatisticsSchema().dump(data_for_statistic)
    return jsonify(result)


@api_blueprint.route('/note_editors/<int:id>', methods=['GET'])
def get_note_editors(id):
    session = Session()

    stat_find = session.query(NoteStatistics).filter_by(noteId=id).all()
    if not stat_find:
        return {"message": "Note with such id does not exists"}, 400

    result = {'editors': []}
    for stat in stat_find:
        result['editors'].append(stat.userId)
    return jsonify(result)
