from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from waitress import serve
from flask_bcrypt import Bcrypt
from blueprint import api_blueprint
from flask_cors import CORS

STUDENT_ID = 2

api = Flask(__name__)
api.register_blueprint(api_blueprint)
bcrypt = Bcrypt(api)
jwt = JWTManager(api)
api.config["JWT_SECRET_KEY"] = "super-secret"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
CORS(api, resources={r"/api/*:": {"origins": "*"}})
api.config['CORS HEADERS'] = 'Content-Type'


@api.route('/api/v1/hello-world-2')
def hello():
    return f'Hello, World {STUDENT_ID}!'


if __name__ == "__main__":
    # api.run('0.0.0.0')
    # serve(api, port=5000)
    api.run(debug=True, port=5000)

# waitress-serve --port=5000 myapp:api

# http://localhost:5000/api/v1/hello-world-3

