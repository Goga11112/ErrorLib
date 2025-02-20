from datetime import timedelta
from flask import Flask, abort, render_template, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager

from database.db import db
from controllers.error_controller import (
    create_error, 
    update_error, 
    delete_error, 
    get_error, 
    get_errors
)
from controllers.auth_controller import register, login, check_auth, view_logs
from controllers.user_controller import create_user
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)

# Настройки сессий
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SESSION_COOKIE_SECURE=False,  # Для локальной разработки
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    SESSION_COOKIE_NAME='flask_session',
    SESSION_REFRESH_EACH_REQUEST=True
)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"
login_manager.login_view = 'login_page'

# Настройки приложения
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.getenv('UPLOAD_FOLDER'))

# Настройки CORS
CORS(app, supports_credentials=True)

# Инициализация базы данных
db.init_app(app)
migrate = Migrate(app, db)

# Создаем папку uploads, если она не существует
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Регистрация маршрутов
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
    next_url = request.args.get('next', '/')
    return render_template('login.html', next_url=next_url)


@app.route('/users')
def users_page():
    return render_template('users.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/logs')
def logs_page():
    return view_logs()

@login_manager.user_loader
def load_user(user_id):
    from database.models.user import User
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    from flask_login import current_user
    return dict(current_user=current_user)

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
