from flask import request, jsonify
from flask_login import current_user
from database.models.user import User
from database.db import db
from services.admin_log_service import AdminLogService


def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    user = User(username=data['username'], is_admin=data.get('is_admin', False))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    AdminLogService.log_action(
        current_user.id,
        user.id,
        'create',
        {'username': user.username, 'is_admin': user.is_admin}
    )

    return jsonify({'message': 'User created successfully'}), 201
