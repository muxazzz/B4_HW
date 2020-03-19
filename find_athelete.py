import uuid
from datetime import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

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

def print_users_list(users_cnt, user_ids, users_all, user_rost):
    """
    Выводит на экран количество найденных пользователей, их идентификатор и время последней активности.
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_ids:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", users_cnt)
        # легенду будущей таблицы
        print("Дата рождения пользователя:")
        # проходимся по каждому идентификатору
        datetime_object0 = datetime.strptime(user_ids[0], '%d/%m/%Y').date()
        for user_id in user_ids:
            # выводим на экран идентификатор — время_последней_активности
            print("{}".format(user_id))
        
        empty_date = {}
        empty_rost = {}
        value = datetime_object0
        for items0 in users_all:
            datetime_object1 = datetime.strptime(items0.birthdate, '%d/%m/%Y').date()
            nearest_date = value - datetime_object1
            empty_date ["Ближайший атлет по дате рождения имеет ID:", items0.id, "Фамилия, имя:", items0.first_name, items0.last_name] = nearest_date
            
        for items1 in users_all:
            nearest_rost = user_rost[0] - items1.height
            empty_rost ["Ближайший атлет по росту имеет ID:", items1.id, "Фамилия, имя:", items1.first_name, items1.last_name] = nearest_rost
        
        print(min(empty_rost.keys(), key=(lambda k: abs(empty_rost[k]))))
        print(min(empty_date.keys(), key=(lambda k: abs(empty_date[k]))))


    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")
    


def find(ids, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
    # По заданному имени пользователя name мы производим фильтрацию таблицы User по полю first_name, 
    # в котором хранится имя каждого пользователя. Специальный метод объекта сессии query принимает на вход 
    # модель данных для поиска (мы подставили в качестве первого аргумента модель User). Он возвращает
    # объект, с помощью которого можно отфильтровать нужные нам строки таблицы, связанной с моделью User.
    # Затем для фильтрации мы используем метод filter, в который можно передать необходимое условие: поле 
    # first_name совпадает с указанным именем name. Так как колонка first_name имеет тип Text, соответствующее условие выглядит следующим образом:
    # User.first_name == name
    query = session.query(User).filter(User.id == ids)
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.birthdate for user in query.all()]
    user_rost = [user.height for user in query.all()]
    users_all = session.query(User).filter(User.id != ids)
    # находим все записи в таблице LastSeenLog, у которых идентификатор совпадает с одним из найденных
    # Метод filter возвращает нам объект типа Query, который предоставляет набор удобных методов для работы с результатом фильтрации.
    
    
    return (users_cnt, user_ids, users_all, user_rost)



def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    # выбран режим поиска, запускаем его
    ids = input("Введи имя пользователя для поиска: ")
    # вызываем функцию поиска по имени
    users_cnt, user_ids, users_all, user_rost = find(ids, session)
    # вызываем функцию печати на экран результатов поиска
    print_users_list(users_cnt, user_ids, users_all, user_rost)

if __name__ == "__main__":
    main()