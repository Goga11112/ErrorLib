from flask import Flask, request, jsonify, send_from_directory, render_template, abort, redirect, url_for
from flask_cors import CORS
from flask_migrate import Migrate
from db import db
from controllers.error_controller import create_error, update_error, delete_error, get_error, get_errors
from controllers.auth_controller import register, login, check_auth
from controllers.user_controller import create_user
from dotenv import load_dotenv
import os
# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.getenv('UPLOAD_FOLDER'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# Создаем папку uploads, если она не существует
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Регистрируем маршруты
app.route('/api/errors', methods=['POST'])(create_error)
app.route('/api/errors/<int:error_id>', methods=['PUT'])(update_error)
app.route('/api/errors/<int:error_id>', methods=['DELETE'])(delete_error)
app.route('/api/errors/<int:error_id>', methods=['GET'])(get_error)
app.route('/api/errors', methods=['GET'])(get_errors)
app.route('/api/register', methods=['POST'])(register)
app.route('/api/login', methods=['POST'])(login)
app.route('/api/check-auth', methods=['GET'])(check_auth)
app.route('/api/users', methods=['POST'])(create_user)

# Маршруты для страниц
@app.route('/')
def index():
    return render_template('helpError.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/users')
def users_page():
    return render_template('users.html')


@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)