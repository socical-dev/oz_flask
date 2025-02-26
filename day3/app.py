"""
설치할 라이브러리
* flask
* Flask-SQLAlchemy
* flask_sqlalchemy
* pymysql
* db
"""

from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import User, Board
import yaml

app = Flask(__name__)

with open('./db.yaml', 'r') as f:
    config = yaml.safe_load(f)  # 파일 가져오기
    
# 데이터베이스 연결 정보
database_config = config.get('database', {})
app.config['SQLALCHEMY_DATABASE_URI'] = database_config.get('uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# bluepring 설정 및 등록
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

from routes.users import user_blp
from routes.board import board_blp

api = Api(app)
api.register_blueprint(user_blp)
api.register_blueprint(board_blp)

from flask import render_template
@app.route('/manage-boards')
def manage_boards():
    return render_template('boards.html')

@app.route('/manage-users')
def manage_users():
    return render_template('users.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)