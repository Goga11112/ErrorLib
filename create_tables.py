from app import db, app

def create_tables():
    with app.app_context():
        db.create_all()
        print("Таблицы успешно созданы.")
        print("Созданы таблицы: Error, ErrorImage")

if __name__ == "__main__":
    create_tables()
