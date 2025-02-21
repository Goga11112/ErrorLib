from datetime import datetime
from flask import app, request, jsonify
import datetime

from flask_login import current_user
from database.models.user import User
from database.db import db
from services.admin_log_service import AdminLogService


def create_user():
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'}), 415
        
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

            
        missing_fields = []
        if not data.get('username'):
            missing_fields.append('username')
        if not data.get('password'):
            missing_fields.append('password')
        if not data.get('realname'):
            missing_fields.append('realname')
            
        if missing_fields:
            return jsonify({
                'message': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400



    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'message': 'Username already exists',
            'username': data['username']
        }), 400


    try:
        user = User(
            username=data['username'],
            realname=data['realname'],
            is_admin=data.get('is_admin', False)
        )

        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error creating user',
            'error': str(e)
        }), 500

    
    AdminLogService.log_action(
        current_user.id,
        user.id,
        'create',
        {'username': user.username, 'is_admin': user.is_admin}
    )

    return jsonify({'message': 'User created successfully'}), 201


def delete_user(user_id):
    """Удаление пользователя администратором"""
    try:
        if not current_user.is_authenticated:
            return jsonify({'message': 'Требуется авторизация'}), 401
            
        if not current_user.is_admin:
            return jsonify({'message': 'Только администратор может удалять пользователей'}), 403

        if current_user.id == user_id:
            return jsonify({'message': 'Нельзя удалить самого себя'}), 400


        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'message': 'Пользователь не найден',
                'details': {
                    'user_id': user_id,
                    'timestamp': datetime.datetime.now().isoformat()
                }
            }), 404


        # Delete associated admin logs
        from database.models.admin_log import AdminLog
        AdminLog.query.filter_by(user_id=user_id).delete()




        # Perform deletion
        db.session.delete(user)
        db.session.commit()

        
        # Log the action
        AdminLogService.log_action(
            current_user.id,
            None,  # error_id is None for user operations
            'delete',
            {
                'username': user.username,
                'deleted_user_id': user_id
            }
        )


        return jsonify({
            'message': 'Пользователь успешно удален',
            'details': {
                'user_id': user_id,
                'timestamp': datetime.datetime.now().isoformat()
            }
        }), 200


    except Exception as e:
        db.session.rollback()
    # Log the detailed error
    import traceback
    error_message = f"Error deleting user {user_id}: {str(e)}\n{traceback.format_exc()}"
    from flask import current_app
    current_app.logger.error(error_message)

    return jsonify({
            'message': 'Ошибка при удалении пользователя',
            'details': {
                'error': str(e),
                'user_id': user_id,
                'timestamp': datetime.datetime.now().isoformat()
            }
        }), 500







def get_users():
    """Получение списка всех пользователей"""
    if not current_user.is_admin:
        return jsonify({'message': 'Только администратор может просматривать список пользователей'}), 403

    users = User.query.all()
    users_data = [{
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    } for user in users]

    return jsonify(users_data), 200
