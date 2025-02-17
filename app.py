import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Goga:191202@localhost/db_errors'
app.config['UPLOAD_FOLDER'] = 'F:/Progect/errorHelp/uploads'
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ErrorImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    error_id = db.Column(db.Integer, db.ForeignKey('error.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("type IN ('error', 'solution')", name='type_check'),
    )

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    solution = db.Column(db.Text, nullable=False)
    images = db.relationship('ErrorImage', backref='error', cascade='all, delete-orphan')

@app.route('/')
def index():
    return render_template('helpError.html')

@app.route('/api/errors', methods=['POST'])
def create_error():
    data = request.form
    error_files = request.files.getlist('errorImageFiles')
    solution_files = request.files.getlist('solutionImageFiles')
    
    # Проверка форматов файлов
    for files in [error_files, solution_files]:
        for image_file in files:
            if not (image_file.filename.endswith('.png') or image_file.filename.endswith('.jpg') or image_file.filename.endswith('.jpeg')):
                return jsonify({'message': 'Недопустимый формат файла. Допустимы только .png и .jpg'}), 400
    
    try:
        new_error = Error(name=data['errorName'], solution=data['errorSolution'])
        
        # Сохранение изображений ошибок
        for image_file in error_files:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            error_image = ErrorImage(filename=filename, type='error', error=new_error)
            db.session.add(error_image)
        
        # Сохранение изображений решений
        for image_file in solution_files:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            error_image = ErrorImage(filename=filename, type='solution', error=new_error)
            db.session.add(error_image)

        db.session.add(new_error)
        db.session.commit()
        return jsonify({'message': 'Error created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Ошибка с таким названием уже существует'}), 400

@app.route('/api/errors/<int:error_id>', methods=['PUT'])
def update_error(error_id):
    data = request.form
    error = Error.query.get_or_404(error_id)
    
    try:
        if error.name != data['errorName']:
            error.name = data['errorName']
        error.solution = data['errorSolution']
        
        if 'errorImageFiles' in request.files or 'solutionImageFiles' in request.files:
            error_files = request.files.getlist('errorImageFiles')
            solution_files = request.files.getlist('solutionImageFiles')
            
            # Удаление старых изображений
            for image in error.images:
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image.filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                db.session.delete(image)
            
            # Сохранение новых изображений ошибок
            for image_file in error_files:
                if image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    error_image = ErrorImage(filename=filename, type='error', error=error)
                    db.session.add(error_image)
            
            # Сохранение новых изображений решений
            for image_file in solution_files:
                if image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    error_image = ErrorImage(filename=filename, type='solution', error=error)
                    db.session.add(error_image)

        db.session.commit()
        return jsonify({'message': 'Error updated successfully'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Ошибка с таким названием уже существует'}), 400

@app.route('/api/errors/<int:error_id>', methods=['DELETE'])
def delete_error(error_id):
    error = Error.query.get_or_404(error_id)
    for image in error.images:
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image.filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))

    db.session.delete(error)    
    db.session.commit()
    return jsonify({'message': 'Error deleted successfully'})

@app.route('/api/errors/<int:error_id>', methods=['GET'])
def get_error(error_id):
    error = Error.query.get_or_404(error_id)
    return jsonify({
        'id': error.id,
        'name': error.name,
        'error_images': [img.filename for img in error.images if img.type == 'error'],
        'solution_images': [img.filename for img in error.images if img.type == 'solution'],
        'solution': error.solution
    })

@app.route('/api/errors', methods=['GET'])
def get_errors():
    errors = Error.query.all()
    return jsonify([{
        'id': error.id,
        'name': error.name,
        'error_images': [img.filename for img in error.images if img.type == 'error'],
        'solution_images': [img.filename for img in error.images if img.type == 'solution'],
        'solution': error.solution
    } for error in errors])

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
