from app import app, db

with app.app_context():
    # Сначала удаляем записи из error_image
    db.session.query(db.Model.metadata.tables['error_image']).delete()
    # Затем удаляем записи из error
    db.session.query(db.Model.metadata.tables['error']).delete()
    db.session.commit()
    print("Таблицы error и error_image успешно очищены")
