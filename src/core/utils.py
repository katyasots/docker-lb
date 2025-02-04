from src.core.db import db
from src.core.models import *


def drop_tables():
    try:
        with db:
            db.drop_tables([Subscription])
            db.drop_tables([Publication])
            db.drop_tables([Subscriber])
            db.drop_tables([District])
            db.drop_tables([Postman])

    except Exception as e:
        print(f"Ошибка при удалении таблиц: {e}")


def create_tables():
    try:
        with db:
            db.create_tables([Postman])
            db.create_tables([District])
            db.create_tables([Subscriber])
            db.create_tables([Publication])
            db.create_tables([Subscription])

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


def connect_db():
    try:
        db.connect()
    except Exception as e:
        print(f"Невозможно подключиться к базе данных: {e}")


def close_db():
    try:
        db.close()
    except Exception as e:
        print(f"Невозможно закрыть соединение с базой данных: {e}")


def migrate():
    connect_db()
    drop_tables()
    create_tables()
    close_db()


if __name__ == '__main__':
    migrate()
