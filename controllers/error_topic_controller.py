from flask import request, jsonify
from flask_login import login_required, current_user
from database.models.error_topic import ErrorTopic
from database.db import db

@login_required
def create_error_topic():
    if not current_user.is_admin:
        return jsonify({'message': 'Доступ запрещен'}), 403
        
    data = request.get_json()
    if not data or not data.get('topic') or not data.get('responsible') or not data.get('phone'):
        return jsonify({'message': 'Необходимо указать тему, ответственного и телефон'}), 400

    error_topic = ErrorTopic(
        topic=data['topic'],
        responsible=data['responsible'],
        phone=data['phone']
    )
    db.session.add(error_topic)
    db.session.commit()
    return jsonify({'message': 'Тема ошибки создана'}), 201

@login_required
def get_error_topics():
    error_topics = ErrorTopic.query.all()
    return jsonify([{
        'id': et.id,
        'topic': et.topic,
        'responsible': et.responsible,
        'phone': et.phone
    } for et in error_topics])

@login_required
def get_error_topic(error_topic_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Доступ запрещен'}), 403
        
    error_topic = ErrorTopic.query.get(error_topic_id)
    if not error_topic:
        return jsonify({'message': 'Тема ошибки не найдена'}), 404

    return jsonify({
        'id': error_topic.id,
        'topic': error_topic.topic,
        'responsible': error_topic.responsible,
        'phone': error_topic.phone
    })

@login_required
def update_error_topic(error_topic_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Доступ запрещен'}), 403
        
    error_topic = ErrorTopic.query.get(error_topic_id)
    if not error_topic:
        return jsonify({'message': 'Тема ошибки не найдена'}), 404

    data = request.get_json()
    if 'topic' in data:
        error_topic.topic = data['topic']
    if 'responsible' in data:
        error_topic.responsible = data['responsible']
    if 'phone' in data:
        error_topic.phone = data['phone']

    db.session.commit()
    return jsonify({'message': 'Тема ошибки обновлена'})

@login_required
def delete_error_topic(error_topic_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Доступ запрещен'}), 403
        
    error_topic = ErrorTopic.query.get(error_topic_id)
    if not error_topic:
        return jsonify({'message': 'Тема ошибки не найдена'}), 404

    db.session.delete(error_topic)
    db.session.commit()
    return jsonify({'message': 'Тема ошибки удалена'})
