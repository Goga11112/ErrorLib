from datetime import datetime
from database.db import db
from sqlalchemy import event

class AdminLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    error_id = db.Column(db.Integer, db.ForeignKey('error.id'), nullable=False)
    action_type = db.Column(db.String(10), nullable=False)  # create/update/delete
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    details = db.Column(db.JSON, nullable=True)

    user = db.relationship('User', backref='admin_logs')
    error = db.relationship('Error', backref='admin_logs')

    def __repr__(self):
        return f'<AdminLog {self.id} {self.action_type} {self.timestamp}>'

    @staticmethod
    def log_action(user_id, error_id, action_type, details=None):
        """Create a new admin log entry"""
        log = AdminLog(
            user_id=user_id,
            error_id=error_id,
            action_type=action_type,
            details=details
        )
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_logs_for_user(user_id):
        """Get all logs for a specific user"""
        return AdminLog.query.filter_by(user_id=user_id).order_by(AdminLog.timestamp.desc()).all()

    @staticmethod
    def get_logs_for_error(error_id):
        """Get all logs for a specific error"""
        return AdminLog.query.filter_by(error_id=error_id).order_by(AdminLog.timestamp.desc()).all()
