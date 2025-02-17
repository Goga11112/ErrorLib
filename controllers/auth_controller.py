from flask import request, jsonify
from models.user import User
from db import db

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
