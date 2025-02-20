from datetime import datetime
from database.models.admin_log import AdminLog

class AdminLogService:
    @staticmethod
    def log_action(user_id, error_id, action_type, details=None):
        """Логирует действие администратора"""
        return AdminLog.log_action(user_id, error_id, action_type, details)

    @staticmethod
    def get_user_actions(user_id):
        """Возвращает действия пользователя"""
        return AdminLog.get_logs_for_user(user_id)

    @staticmethod
    def get_error_actions(error_id):
        """Возвращает действия с ошибкой"""
        return AdminLog.get_logs_for_error(error_id)

    @staticmethod
    def get_recent_actions(limit=100):
        """Возвращает последние действия"""
        return AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(limit).all()
