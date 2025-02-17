from app import db, Error

# Заполнение таблицы начальными данными
def seed_data():
    error1 = Error(name="Ошибка 404", image="error404.png", solution="Страница не найдена.")
    error2 = Error(name="Ошибка 500", image="error500.png", solution="Внутренняя ошибка сервера.")
    
    db.session.add(error1)
    db.session.add(error2)
    db.session.commit()
    print("Начальные данные успешно добавлены.")

if __name__ == "__main__":
    seed_data()
