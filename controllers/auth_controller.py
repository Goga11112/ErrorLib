from flask import abort, request, jsonify, render_template
from flask_login import current_user, login_required, login_user, logout_user
from database.models.user import User
from database.db import db
from services.admin_log_service import AdminLogService
from database.models.admin_log import AdminLog

def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        AdminLogService.log_action(
            None,
            'failed_register',
            None,
            {'error': 'Missing username or password'}
        )
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=data['username']).first():
        AdminLogService.log_action(
            None,
            'failed_register',
            None,
            {'error': 'Username already exists', 'username': data['username']}
        )
        return jsonify({'message': 'Username already exists'}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    user.is_admin=data['is_admin']
    user.realname=data['realname']
    db.session.add(user)
    db.session.commit()
    
    AdminLogService.log_action(
        current_user.id if current_user.is_authenticated else None,
        'create',
        None,
        {
            'username': user.username,
            'is_admin': user.is_admin,
            'realname': user.realname
        }
    )

    return jsonify({'message': 'User registered successfully'}), 201

def login():
    try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            AdminLogService.log_action(
                None,
                'failed_login',
                None,
                {'error': 'Missing credentials'}
            )
            return jsonify({'message': 'Authentication required'}), 401

        user = User.query.filter_by(username=auth.username).first()
        if user and user.check_password(auth.password):
            login_user(user)
            AdminLogService.log_action(
                user.id,
                'successful_login',
                None,
                {'username': auth.username}
            )
            return jsonify({
                'message': 'Login successful', 
                'is_admin': user.is_admin,
                'user_id': user.id
            }), 200

        AdminLogService.log_action(
            None,
            'failed_login',
            None,
            {
                'username': auth.username,
                'reason': 'Invalid credentials'
            }
        )

        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        AdminLogService.log_action(
            None,
            'login_error',
            None,
            {'error': str(e)}
        )
        return jsonify({'message': 'Internal server error'}), 500

def check_auth():
    try:
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True,
                'is_admin': current_user.is_admin,
                'username': current_user.username
            })
        return jsonify({'authenticated': False})
    except Exception as e:
        return jsonify({'authenticated': False}), 500

@login_required
def view_logs():
    if not current_user.is_authenticated:
        abort(401)
        
    logs = AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(100).all()
    return render_template('logs.html', logs=logs)
