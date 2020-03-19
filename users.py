# импортируем модули стандартной библиотеки uuid и datetime

import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

"""
class Athlet(Base):
	__tablename__ = 'athelete'
	id = sa.Column(sa.INTEGER, primary_key=True)
	age = sa.Column(sa.INTEGER)
	gender = sa.Column(sa.TEXT)
	gold_medals = sa.Column(sa.INTEGER)

engine = sa.create_engine(DB_PATH)
sessions = sessionmaker(engine)
session = sessions()

atheletes = session.query(Athlet).filter(Athlet.gender=="Female").count()
atheletes_age = session.query(Athlet).filter(Athlet.age > 30).count()
atheletes_gold = session.query(Athlet).filter(Athlet.age > 25, Athlet.gender == "Male", Athlet.gold_medals >= 2).count()
print(atheletes, atheletes_age, atheletes_gold)
"""


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.TEXT)
    # фамилия пользователя
    last_name = sa.Column(sa.TEXT)
    # адрес электронной почты пользователя
    email = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Пол: ")
    email = input("email: ")
    birthdate = input("дата рождения: ")
    height = input("рост: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
   
    # создаем нового пользователя
    user = User(
     
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )

    return user


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
        # запрашиваем данные пользоватлея
    user = request_data()
        # добавляем нового пользователя в сессию
    session.add(user)
        # обновляем время последнего визита для этого пользователя
        # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")
   

if __name__ == "__main__":
    main()