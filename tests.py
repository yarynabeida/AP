import base64
import json
import pytest
from myapp import *
from blueprint import *
from models import User
from datetime import datetime
user_0 = User(name="Maria", email="maria@gmail.com", password=Bcrypt().generate_password_hash("1233345").decode('utf - 8'))
user_1 = User(name="Mia", email="mia@gmail.com", password=Bcrypt().generate_password_hash("12345").decode('utf - 8'))
user_2 = User(name="Andrii", email="andrii@gmail.com", password=Bcrypt().generate_password_hash("1923").decode('utf - 8'))
user_3 = User(name="Oleg", email="oleg@gmail.com", password=Bcrypt().generate_password_hash("19ee23").decode('utf - 8'))
tag_2 = Tag(name='#tag2000')
tag_3 = Tag(name='todolist')
tag_4 = Tag(name='todosmth')


def test_register_user():
    session.add(user_0)
    client = api.test_client()
    url = "http://localhost:5000/user"
    user_data_json = "{\n \"name\": \"yulia\", \"email\": \"yulia@gmail.com\", \"password\": \"123456\" \n}"
    user_invalid_data_json = "{\n \"name\": 2, \"email\": \"yulia@gmail.com\", \"password\": \"123456\" \n}"
    user_invalid_username_json = "{\n \"name\": \"Mia\", \"email\": \"yulia@gmail.com\", \"password\": \"12345\" \n}"
    user_invalid_email_json = "{\n \"name\": \"yulia\", \"email\": \"mia@gmail.com\", \"password\": \"12345\" \n}"
    user_id_json = "{\n \"id\": \"1\",\"name\": \"yulia\", \"email\": \"mia@gmail.com\", \"password\": \"12345\" \n}"
    headers = {'Content-Type': 'application/json'}
    response = client.post(url, headers=headers, data=user_data_json)
    user_find = session.query(User).filter_by(name="yulia").first()
    assert response.status_code == 200
    assert user_find.email == "yulia@gmail.com"
    response = client.post(url, headers=headers, data=user_invalid_username_json)
    assert response.status_code == 400
    response = client.post(url, headers=headers, data=user_id_json)
    assert response.status_code == 401
    response = client.post(url, headers=headers, data=user_invalid_email_json)
    assert response.status_code == 400
    response = client.post(url, headers=headers, data=user_invalid_data_json)
    assert response.status_code == 422
    session.delete(user_0)
    session.delete(user_find)
    session.commit()


@pytest.fixture(scope="module")
def create_user():
    user = User(name="yulia", email="yulia@gmail.com", password=Bcrypt().generate_password_hash("123456").decode('utf - 8'))
    session.add(user)
    session.commit()
    yield
    session.delete(user)
    session.commit()


def test_login_user(create_user):
    client = api.test_client()
    url = "http://localhost:5000/user/login"
    valid_credentials = base64.b64encode(b"yulia:123456").decode("utf-8")
    wrong_username_valid_credentials = base64.b64encode(b"misha:123456").decode("utf-8")
    wrong_password_valid_credentials = base64.b64encode(b"yulia:12345677").decode("utf-8")
    response = client.get(url, headers={"Authorization": "Basic " + valid_credentials})
    assert response.status_code == 200
    response = client.get(url, headers={"Authorization": "Basic " + wrong_username_valid_credentials})
    assert response.status_code == 404
    response = client.get(url, headers={"Authorization": "Basic " + wrong_password_valid_credentials})
    assert response.status_code == 400


@pytest.fixture
def login_user(create_user):
    valid_credentials = base64.b64encode(b"yulia:123456").decode("utf-8")
    test_client = api.test_client()
    url = "http://localhost:5000/user/login"
    headers = {"Authorization": "Basic " + valid_credentials}
    response = test_client.get(url, headers=headers)
    access_token_data_login_json = json.loads((response.get_data(as_text=True)))
    return access_token_data_login_json


@pytest.fixture(scope="module")
def get_tokens():
    session.add(user_1)
    session.add(user_2)
    session.commit()
    client = api.test_client()
    valid_credentials_1 = base64.b64encode(b"Mia:12345").decode("utf-8")
    valid_credentials_2 = base64.b64encode(b"Andrii:1923").decode("utf-8")
    response_1 = client.get("/user/login", headers={"Authorization": "Basic " + valid_credentials_1})
    response_2 = client.get("/user/login", headers={"Authorization": "Basic " + valid_credentials_2})
    yield [json.loads(response_1.get_data(as_text=True)), json.loads(response_2.get_data(as_text=True))]
    session.delete(user_1)
    session.commit()
    session.delete(user_2)
    session.commit()


def test_update_user(get_tokens):
    client = api.test_client()
    token1 = get_tokens[0]['token']
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token1}
    headers_invalid = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    user = session.query(User).filter_by(id=user_1.id).first()
    url = "http://localhost:5000/user/"+str(user.id)
    invalid_url = "http://localhost:5000/user/988"
    update_data_json = "{\n \"name\": \"Mia2\", \"email\": \"oleg@gmail.com\", \"password\": \"12345678\" \n}"
    update_name_data_json = "{\n \"name\": \"Mia\", \"email\": \"oleg@gmail.com\", \"password\": \"12345678\" \n}"
    update_email_data_json = "{\n \"name\": \"oleg\", \"email\": \"andrii@gmail.com\", \"password\": \"12345678\" \n}"
    update_id_data_json = "{\n \"id\": \"2\", \"name\": \"oleg\", \"email\": \"andrii@gmail.com\", \"password\": \"12345678\" \n}"
    response = client.put(url, headers=headers, data=update_data_json)
    assert response.status_code == 200
    response = client.put(url, headers=headers, data=update_id_data_json)
    assert response.status_code == 401
    response = client.put(invalid_url, headers=headers, data=update_data_json)
    assert response.status_code == 400
    response = client.put(url, headers=headers, data=update_name_data_json)
    assert response.status_code == 400
    response = client.put(url, headers=headers, data=update_email_data_json)
    assert response.status_code == 400
    response = client.put(url, headers=headers_invalid, data=update_data_json)
    assert response.status_code == 403


@pytest.fixture(scope="module")
def create_tags():
    session.add(tag_2)
    session.add(tag_3)
    session.add(tag_4)
    session.commit()
    yield
    session.delete(tag_2)
    session.delete(tag_3)
    session.delete(tag_4)
    session.commit()


def test_create_note(get_tokens, create_tags):
    session.add(user_2)
    session.commit()
    tag = session.query(Tag).filter_by(name=tag_2.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    client = api.test_client()
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    url = "http://localhost:5000/note"
    data_json = "{\n \"name\": \"What to read\",\n \"text\": \"Lorem ipsum dolor sit amet\",\n \"idTag\": " + str(tag_id) + ", \n \"idOwner\": " + str(user_id) + " \n}"
    data_duplicate_json = "{\n \"name\": \"What to read\", \n \"idTag\": " + str(tag_id) + ", \n \"idOwner\": " + str(user_id) + " \n}"
    data_tag_json = "{\n \"name\": \"What to read\",\n \"text\": \"Lorem ipsum dolor sit amet\",\n \"idTag\": \"238\" ,\n " + str(user_id) + " \n}"
    data_owner_json = "{\n \"name\": \"What to read\",\n \"text\": \"Lorem ipsum dolor sit amet\",\n \"idTag\": " + str(tag_id) + ", \n \"idTag\": \"238\"  \n}"
    data_id_json = "{\n \"id\": \"1\",\"name\": \"What to read\",\n \"text\": \"Lorem ipsum dolor sit amet\",\n \"idTag\": " + str(tag_id) + ", \n \"idOwner\": " + str(user_id) + " \n}"
    data_valid_json = "{\n \"name\": 2,\n \"text\": \"Lorem ipsum dolor sit amet\",\n \"idTag\": " + str(tag_id) + ", \n \"idOwner\": " + str(user_id) + " \n}"
    response = client.post(url, headers=headers, data=data_json)
    assert response.status_code == 200
    assert response.json['name'] == "What to read"
    response = client.post(url, headers=headers, data=data_valid_json)
    assert response.status_code == 422
    response = client.post(url, headers=headers, data=data_duplicate_json)
    assert response.status_code == 400
    response = client.post(url, headers=headers, data=data_id_json)
    assert response.status_code == 401
    response = client.post(url, headers=headers, data=data_tag_json)
    assert response.status_code == 400
    response = client.post(url, headers=headers, data=data_owner_json)
    assert response.status_code == 400
    note_find = session.query(Note).filter_by(name="What to read").first()
    note_stat = session.query(NoteStatistics).filter_by(noteId=note_find.id).first()
    session.delete(note_stat)
    session.commit()
    session.delete(note_find)
    session.commit()


def test_get_note(create_tags):
    session.add(user_3)
    session.commit()
    tag = session.query(Tag).filter_by(name=tag_3.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_3.name).first()
    user_id = user.id
    note_1 = Note(name="wash", text="to do", idTag=tag_id, idOwner=user_id)
    session.add(note_1)
    session.commit()
    note = session.query(Note).filter_by(name="wash").first()
    note_id = note.id
    url = "http://localhost:5000/note/"+str(note_id)
    invalid_url = "http://localhost:5000/note/10000"
    client = api.test_client()
    response = client.get(url)
    assert response.status_code == 200
    response = client.get(invalid_url)
    assert response.status_code == 404
    session.delete(user)
    session.delete(note)
    session.commit()


def test_delete_note(get_tokens, create_tags):
        session.add(user_2)
        session.commit()
        client = api.test_client()
        token2 = get_tokens[1]['token']
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
        tag = session.query(Tag).filter_by(name=tag_4.name).first()
        tag_id = tag.id
        user = session.query(User).filter_by(name=user_2.name).first()
        user_id = user.id
        note_2 = Note(name="job", text="to do", idTag=tag_id, idOwner=user_id)
        session.add(note_2)
        session.commit()
        note_to = session.query(Note).filter_by(name="job").first()
        note_id = note_to.id
        note_stat = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_id)
        session.add(note_stat)
        session.commit()
        url = "http://localhost:5000/note/"+str(note_id)
        invalid_url = "http://localhost:5000/note/1000"
        response = client.delete(url, headers=headers)
        assert response.status_code == 200
        response = client.delete(invalid_url, headers=headers)
        assert response.status_code == 404
        session.delete(note_stat)
        session.delete(note_to)
        session.commit()


def test_get_service(create_tags):
    client = api.test_client()
    session.add(user_2)
    session.commit()
    tag = session.query(Tag).filter_by(name=tag_4.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    note_2 = Note(name="job", text="to do", idTag=tag_id, idOwner=user_id)
    session.add(note_2)
    session.commit()
    url = "http://localhost:5000/note_service"
    response = client.get(url)
    assert response.status_code == 200
    session.delete(note_2)
    session.commit()


def test_get_user_note(get_tokens, create_tags):
    session.add(user_2)
    session.commit()
    client = api.test_client()
    token1 = get_tokens[0]['token']
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    invalid_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token1}
    tag = session.query(Tag).filter_by(name=tag_2.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    note_2 = Note(name="job", text="to do", idTag=tag_id, idOwner=user_id)
    session.add(note_2)
    session.commit()
    note_to = session.query(Note).filter_by(name="job").first()
    note_id = note_to.id
    note_stat = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_id)
    session.add(note_stat)
    session.commit()
    url = "http://localhost:5000/note_service/"+str(user_id)
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    response = client.get(url, headers=invalid_headers)
    assert response.status_code == 403
    session.delete(note_to)
    session.delete(note_stat)
    session.commit()


def test_get_note_editors(get_tokens, create_tags):
    session.add(user_2)
    session.commit()
    client = api.test_client()
    token1 = get_tokens[0]['token']
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    invalid_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token1}
    tag = session.query(Tag).filter_by(name=tag_2.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    note_2 = Note(name="job", text="to do", idTag=tag_id, idOwner=user_id)
    session.add(note_2)
    session.commit()
    note_to = session.query(Note).filter_by(name="job").first()
    note_id = note_to.id
    note_stat = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_id)
    session.add(note_stat)
    session.commit()
    url = "http://localhost:5000/note_editors/"+str(note_id)
    invalid_url = "http://localhost:5000/note_editors/"
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    response = client.get(url, headers=invalid_headers)
    assert response.status_code == 403
    response = client.get(invalid_url, headers=headers)
    assert response.status_code == 404
    session.delete(note_to)
    session.delete(note_stat)
    session.commit()


def test_get_user_statistics(get_tokens, create_tags):
    session.add(user_2)
    session.commit()
    client = api.test_client()
    token1 = get_tokens[0]['token']
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    invalid_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token1}
    tag = session.query(Tag).filter_by(name=tag_2.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    note_3 = Note(name="well", text="title", idTag=tag_id, idOwner=user_id)
    note_4 = Note(name="jakey", text="asadsd", idTag=tag_id, idOwner=user_id)
    session.add(note_3)
    session.add(note_4)
    session.commit()
    note_stat = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_3.id)
    note_stat_1 = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_4.id)
    session.add(note_stat)
    session.add(note_stat_1)
    session.commit()
    url = "http://localhost:5000/userstatistics/"+str(user_id)
    url_invalid = "http://localhost:5000/userstatistics/233"
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    response = client.get(url, headers=invalid_headers)
    assert response.status_code == 403
    response = client.get(url_invalid, headers=headers)
    assert response.status_code == 404
    session.delete(note_3)
    session.delete(note_4)
    session.delete(note_stat)
    session.delete(note_stat_1)
    session.commit()

def test_update_note(get_tokens, create_tags):
    session.add(user_2)
    session.commit()
    client = api.test_client()
    token1 = get_tokens[0]['token']
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    invalid_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token1}
    tag = session.query(Tag).filter_by(name=tag_4.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    note_8 = Note(name="well", text="title", idTag=tag_id, idOwner=user_id)
    session.add(note_8)
    session.commit()
    note_stat = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_8.id)
    session.add(note_stat)
    session.commit()
    note_find = session.query(Note).filter_by(name='well').first()
    note_id = note_find.id
    data_json = "{ \n \"name\": \"note2\" \n}"
    data_json_invalid = "{ \n \"idOwner\": " + str(user_id) + "\n}"
    url = "http://localhost:5000/note/"+str(note_id)
    url_invalid = "http://localhost:5000/note/10000"
    response = client.put(url, headers=headers, data=data_json)
    assert response.status_code == 200
    response = client.put(url, headers=invalid_headers, data=data_json)
    assert response.status_code == 403
    response = client.put(url_invalid, headers=headers, data=data_json)
    assert response.status_code == 404
    response = client.put(url, headers=headers, data=data_json_invalid)
    assert response.status_code == 403
    session.delete(note_stat)
    session.delete(note_8)
    session.commit()


def test_add_user_to_note(get_tokens,create_tags):
    session.add(user_2)
    session.commit()
    client = api.test_client()
    token1 = get_tokens[0]['token']
    token2 = get_tokens[1]['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token2}
    tag = session.query(Tag).filter_by(name=tag_4.name).first()
    tag_id = tag.id
    user = session.query(User).filter_by(name=user_2.name).first()
    user_id = user.id
    note_3 = Note(name="well", text="title", idTag=tag_id, idOwner=user_id)
    note_4 = Note(name="jakey", text="asadsd", idTag=tag_id, idOwner=user_id)
    session.add(note_3)
    session.add(note_4)
    session.commit()
    note_stat = NoteStatistics(time=datetime.today().strftime('%Y-%m-%d'), userId=user_id, noteId=note_3.id)
    session.add(note_stat)
    session.commit()
    user_find = session.query(User).filter_by(name=user_1.name).first()
    id_find = user_find.id
    data_json = "{\n \"userId\": " + str(id_find) + ", \n \"noteId\":" + str(note_3.id) + "\n}"
    data_name_json = "{\n \"userId\": 1000, \n \"noteId\":" + str(note_3.id) + " \n}"
    url = "http://localhost:5000/note_user"
    response = client.post(url, headers=headers, data=data_json)
    note_find = session.query(NoteStatistics).filter_by(userId=id_find).first()
    assert response.status_code == 200
    response = client.post(url, headers=headers)
    assert response.status_code == 400
    response = client.post(url, headers=headers, data=data_name_json)
    assert response.status_code == 400
    session.delete(note_find)
    session.delete(note_3)
    session.delete(note_4)
    session.delete(note_stat)
    session.commit()


def test_delete_user(login_user,get_tokens):
    session.add(user_2)
    session.commit()
    client = api.test_client()
    token = login_user['token']
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    user_find = session.query(User).filter_by(name='yulia').first()
    user_id = user_find.id
    url = "http://localhost:5000/user/"+str(user_id)
    invalid_url = "http://localhost:5000/user/988"
    response = client.delete(url, headers=headers)
    assert response.status_code == 200
    response = client.delete(invalid_url, headers=headers)
    assert response.status_code == 404
    session.delete(user_find)

