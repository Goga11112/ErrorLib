from flask import request, jsonify, current_app
from flask_login import current_user
from database.models.error import Error
from services.admin_log_service import AdminLogService

from database.models.error_image import ErrorImage
from database.db import db
from utils.file_utils import get_unique_filename
from utils.error_utils import check_error_name_exists
import os
from sqlalchemy.exc import IntegrityError

def create_error():
    data = request.form
    error_files = request.files.getlist('errorImageFiles')
    solution_files = request.files.getlist('solutionImageFiles')
    
    if check_error_name_exists(data['errorName']):
        return jsonify({'message': 'Ошибка с таким названием уже существует'}), 400
    
    for files in [error_files, solution_files]:
        for image_file in files:
            if not (image_file.filename.endswith('.png') or 
                   image_file.filename.endswith('.jpg') or 
                   image_file.filename.endswith('.jpeg') or
                   image_file.filename.endswith('.gif')):
                return jsonify({'message': 'Недопустимый формат файла. Допустимы только .png, .jpg и .gif'}), 400
    
    try:
        new_error = Error(name=data['errorName'], solution=data['errorSolution'])
        
        for image_file in error_files:
            if image_file.filename != '':
                filename = get_unique_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                error_image = ErrorImage(filename=filename, type='error', error=new_error)
                db.session.add(error_image)
        
        for image_file in solution_files:
            if image_file.filename != '':
                filename = get_unique_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                error_image = ErrorImage(filename=filename, type='solution', error=new_error)
                db.session.add(error_image)

        db.session.add(new_error)
        db.session.commit()
        AdminLogService.log_action(
            current_user.id,
            new_error.id,
            'create',
            {'name': new_error.name}
        )
        return jsonify({'message': 'Error created successfully'}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Ошибка с таким названием уже существует'}), 400

def update_error(error_id):
    data = request.form
    error = Error.query.get_or_404(error_id)
    
    if error.name != data['errorName'] and check_error_name_exists(data['errorName'], exclude_id=error_id):
        return jsonify({'message': 'Ошибка с таким названием уже существует'}), 400
    
    try:
        error.name = data['errorName']
        error.solution = data['errorSolution']
        
        if 'errorImageFiles' in request.files or 'solutionImageFiles' in request.files:
            error_files = request.files.getlist('errorImageFiles')
            solution_files = request.files.getlist('solutionImageFiles')
            
            for image in error.images:
                if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)):
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
                db.session.delete(image)
            
            for image_file in error_files:
                if image_file.filename != '':
                    filename = get_unique_filename(image_file.filename)
                    image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    error_image = ErrorImage(filename=filename, type='error', error=error)
                    db.session.add(error_image)
            
            for image_file in solution_files:
                if image_file.filename != '':
                    filename = get_unique_filename(image_file.filename)
                    image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    error_image = ErrorImage(filename=filename, type='solution', error=error)
                    db.session.add(error_image)

        db.session.commit()
        AdminLogService.log_action(
            current_user.id,
            error.id,
            'update',
            {'name': error.name}
        )
        return jsonify({'message': 'Error updated successfully'})

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Ошибка с таким названием уже существует'}), 400

def delete_error(error_id):
    error = Error.query.get_or_404(error_id)
    for image in error.images:
        if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)):
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))

    db.session.delete(error)    
    db.session.commit()
    AdminLogService.log_action(
        current_user.id,
        error.id,
        'delete',
        {'name': error.name}
    )
    return jsonify({'message': 'Error deleted successfully'})


def get_error(error_id):
    error = Error.query.get_or_404(error_id)
    return jsonify({
        'id': error.id,
        'name': error.name,
        'error_images': [img.filename for img in error.images if img.type == 'error'],
        'solution_images': [img.filename for img in error.images if img.type == 'solution'],
        'solution': error.solution
    })

def get_errors():
    errors = Error.query.all()
    return jsonify([{
        'id': error.id,
        'name': error.name,
        'error_images': [img.filename for img in error.images if img.type == 'error'],
        'solution_images': [img.filename for img in error.images if img.type == 'solution'],
        'solution': error.solution
    } for error in errors])
