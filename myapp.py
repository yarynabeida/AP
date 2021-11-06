from flask import Flask
from waitress import serve
# from blueprint import api_blueprint

STUDENT_ID = 2

api = Flask(__name__)
# api.register_blueprint(api_blueprint)


@api.route('/api/v1/hello-world-3')
def hello():
    return f'Hello, World {STUDENT_ID}!'


if __name__ == "__main__":
    # api.run('0.0.0.0')
    serve(api, port=5000)

# waitress-serve --port=5000 myapp:api

# http://localhost:5000/api/v1/hello-world-3

# curl -X POST http://localhost:5000/user
