from app import app, db
from models.user import User

def create_tables():
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        print("Таблицы успешно созданы.")
        print("Созданы таблицы: Error, ErrorImage")
        # Создаем пользователя admin
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
            admin_user.set_password('admin')
            admin_user.realname='Егор'
            admin_user.is_admin=True
            
            db.session.add(admin_user)
            db.session.commit()
            print("Пользователь admin создан")
        else:
            print("Пользователь admin уже существует")

if __name__ == '__main__':
    create_tables()
