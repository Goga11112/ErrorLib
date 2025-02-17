from app import db

# Создание таблиц
def create_tables():
    db.create_all()
    print("Таблицы успешно созданы.")

if __name__ == "__main__":
    create_tables()
