import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename  # Import secure_filename
from flask_cors import CORS  # Import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Goga:191202@localhost/db_errors'  # Updated with your database credentials
app.config['UPLOAD_FOLDER'] = 'F:/Progect/errorHelp/uploads'  # Укажите путь к папке для загрузки изображений
CORS(app)  # Enable CORS for the Flask app
db = SQLAlchemy(app)

# Модель для ошибок
class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('helpError.html')  # Отправляем шаблон helpError.html

@app.route('/api/errors', methods=['POST'])
def create_error():
    data = request.form
    image_file = request.files['errorImageFile']  # Получаем файл изображения
    
    # Проверка на допустимые расширения файлов
    if not (image_file.filename.endswith('.png') or image_file.filename.endswith('.jpg') or image_file.filename.endswith('.jpeg')):
        return jsonify({'message': 'Недопустимый формат файла. Допустимы только .png и .jpg'}), 400
    
    filename = secure_filename(image_file.filename)
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Сохраняем файл
    new_error = Error(name=data['errorName'], image=filename, solution=data['errorSolution'])


    db.session.add(new_error)
    db.session.commit()
    return jsonify({'message': 'Error created successfully'}), 201

@app.route('/api/errors/<int:error_id>', methods=['PUT'])
def update_error(error_id):
    data = request.form
    error = Error.query.get_or_404(error_id)
    
    # Обновляем название и решение
    error.name = data['errorName']
    error.solution = data['errorSolution']
    
    # Проверяем, загружен ли новый файл изображения
    if 'errorImageFile' in request.files:
        image_file = request.files['errorImageFile']
        if image_file.filename != '':
            # Удаляем старое изображение
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], error.image)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], error.image))
            # Сохраняем новое изображение
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            error.image = filename  # Обновляем имя файла изображения

    db.session.commit()
    return jsonify({'message': 'Error updated successfully'})


@app.route('/api/errors/<int:error_id>', methods=['DELETE'])
def delete_error(error_id):
    error = Error.query.get_or_404(error_id)
    # Удаляем изображение из папки uploads
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], error.image)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], error.image))
    db.session.delete(error)    

    db.session.commit()
    return jsonify({'message': 'Error deleted successfully'})

@app.route('/api/errors/<int:error_id>', methods=['GET'])
def get_error(error_id):
    error = Error.query.get_or_404(error_id)
    return jsonify({'id': error.id, 'name': error.name, 'image': error.image, 'solution': error.solution})

@app.route('/api/errors', methods=['GET'])
def get_errors():
    errors = Error.query.all()
    return jsonify([{'id': error.id, 'name': error.name, 'image': error.image, 'solution': error.solution} for error in errors])

# Маршрут для обслуживания статических файлов
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('uploads', filename)  # Новый маршрут для доступа к файлам в папке uploads


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаёт таблицы в базе данных
    app.run(debug=True)
