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
            None,
            'failed_register',
            {'error': 'Missing username or password'}
        )
        return jsonify({'message': 'Username and password are required'}), 400


    if User.query.filter_by(username=data['username']).first():
        AdminLogService.log_action(
            None,
            None,
            'failed_register',
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
        AdminLogService.log_action(
            None,
            None,
            'login_attempt',
            {'headers': dict(request.headers)}
        )

        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            print("No auth credentials provided")
            return jsonify({'message': 'Authentication required'}), 401

        user = User.query.filter_by(username=auth.username).first()
        if user and user.check_password(auth.password):
            login_user(user)
            return jsonify({
                'message': 'Login successful', 
                'is_admin': user.is_admin,
                'user_id': user.id
            }), 200

        AdminLogService.log_action(
            None,
            None,
            'failed_login',
            {
                'username': auth.username,
                'reason': 'Invalid credentials'
            }
        )

        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500


def check_auth():
    try:
        print(f"Check auth request received. Current user: {current_user}")
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True,
                'is_admin': current_user.is_admin,
                'username': current_user.username
            })
        return jsonify({'authenticated': False})
    except Exception as e:
        print(f"Error during auth check: {str(e)}")
        return jsonify({'authenticated': False}), 500


@login_required
def view_logs():
    print("Accessing logs...")
    print(f"Current user: {current_user}")
    if not current_user.is_authenticated:
        print("Unauthorized access attempt")
        abort(401)
        
    logs = AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(100).all()
    print(f"Found {len(logs)} logs")
    return render_template('logs.html', logs=logs)
