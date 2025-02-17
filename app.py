import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Goga:191202@localhost/db_errors'
app.config['UPLOAD_FOLDER'] = 'F:/Progect/errorHelp/uploads'
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель для изображений ошибок
class ErrorImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    error_id = db.Column(db.Integer, db.ForeignKey('error.id'), nullable=False)

# Модель для ошибок
class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.Text, nullable=False)
    images = db.relationship('ErrorImage', backref='error', cascade='all, delete-orphan')

@app.route('/')
def index():
    return render_template('helpError.html')

@app.route('/api/errors', methods=['POST'])
def create_error():
    data = request.form
    image_files = request.files.getlist('errorImageFiles')
    
    for image_file in image_files:
        if not (image_file.filename.endswith('.png') or image_file.filename.endswith('.jpg') or image_file.filename.endswith('.jpeg')):
            return jsonify({'message': 'Недопустимый формат файла. Допустимы только .png и .jpg'}), 400
    
    new_error = Error(name=data['errorName'], solution=data['errorSolution'])
    
    for image_file in image_files:
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        error_image = ErrorImage(filename=filename, error=new_error)
        db.session.add(error_image)

    db.session.add(new_error)
    db.session.commit()
    return jsonify({'message': 'Error created successfully'}), 201

@app.route('/api/errors/<int:error_id>', methods=['PUT'])
def update_error(error_id):
    data = request.form
    error = Error.query.get_or_404(error_id)
    
    error.name = data['errorName']
    error.solution = data['errorSolution']
    
    if 'errorImageFiles' in request.files:
        image_files = request.files.getlist('errorImageFiles')
        if any(f.filename != '' for f in image_files):
            for image in error.images:
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image.filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                db.session.delete(image)
            
            for image_file in image_files:
                if image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    error_image = ErrorImage(filename=filename, error=error)
                    db.session.add(error_image)

    db.session.commit()
    return jsonify({'message': 'Error updated successfully'})

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
        'images': [image.filename for image in error.images],
        'solution': error.solution
    })

@app.route('/api/errors', methods=['GET'])
def get_errors():
    errors = Error.query.all()
    return jsonify([{
        'id': error.id,
        'name': error.name,
        'images': [image.filename for image in error.images],
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
