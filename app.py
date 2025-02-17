from flask import Flask, request, jsonify, send_from_directory, render_template, abort
from flask_cors import CORS
from flask_migrate import Migrate
from db import db
from controllers.error_controller import create_error, update_error, delete_error, get_error, get_errors
from controllers.auth_controller import register, login
from controllers.user_controller import create_user
import os

from models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Goga:191202@localhost/db_errors'
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')
app.config['SECRET_KEY'] = 'your-secret-key-here'
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
app.route('/api/users', methods=['POST'])(create_user)

@app.route('/')
def index():
    return render_template('helpError.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Создаем суперпользователя, если его нет
        if not User.query.filter_by(is_admin=True).first():
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
