from flask import request, jsonify
from flask_login import current_user
from database.models.user import User
from database.db import db
from services.admin_log_service import AdminLogService


def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    AdminLogService.log_action(
        current_user.id,
        user.id,
        'create',
        {'username': user.username}
    )

    return jsonify({'message': 'User registered successfully'}), 201


def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Authentication required'}), 401

    user = User.query.filter_by(username=auth.username).first()
    if user and user.check_password(auth.password):
        return jsonify({
            'message': 'Login successful', 
            'is_admin': user.is_admin
        }), 200

    AdminLogService.log_action(
        None,  # No user ID for failed attempts
        None,
        'failed_login',
        {'username': auth.username}
    )
    return jsonify({'message': 'Invalid credentials'}), 401


def check_auth():
    auth = request.authorization
    if not auth:
        return jsonify({'authenticated': False})
        
    user = User.query.filter_by(username=auth.username).first()
    if user and user.check_password(auth.password):
        return jsonify({
            'authenticated': True,
            'is_admin': user.is_admin
        })
    
    return jsonify({'authenticated': False})
