import dataclasses
from typing import List

from excercise10.utilities.db.db_manager import dbManager


@dataclasses.dataclass
class User:
    name: str
    email: str
    password: str
    nickname: str

    def is_valid(self):
        return self.name and self.email and self.password and self.nickname


class UserNotFoundError(Exception):
    pass



class UsersManagement:
    DEFAULT_USER_ID = 1

    _CREATE_TABLE_SQL = "CREATE TABLE if not exists users ( `id` INT AUTO_INCREMENT PRIMARY KEY, `email` varchar(255) UNIQUE KEY NOT NULL, `name` varchar(255) NOT NULL,`nickname` varchar(255) DEFAULT NULL,`password` varchar(255) NOT NULL)"
    _INSERT_USER_SQL = "INSERT IGNORE INTO users (email, name, nickname, password) VALUES (%s, %s, %s, %s)"
    _GET_ALL_USERS_SQL = "SELECT * FROM users"
    _GET_USER_BY_ID_SQL = "SELECT * FROM users WHERE id = %s; "
    _DELETE_USER_SQL = """DELETE FROM users WHERE email = '%s' """
    _UPDATE_USER_SQL = "UPDATE"

    def __init__(self):
        self._create_table()
        self._populate_initial_data()

    @classmethod
    def _create_table(cls):
        result = dbManager.execute(cls._CREATE_TABLE_SQL)
        if not result:
            raise Exception('Failed creating users table', result)

    @classmethod
    def _populate_initial_data(cls):
        users = [
            {"name": "Yossi", "email": "yossi@gmail.com", "password": "111", "nickname": "yossile"},
            {"name": "Yaniv", "email": "yaniv@gmail.com", "password": "222", "nickname": "yanivush"},
            {"name": "Gil", "email": "gil@gmail.com", "password": "123", "nickname": "gilush"},
            {"name": "Yaron", "email": "yaron@gmail.com", "password": "233", "nickname": "yaronush"},
            {"name": "Galit", "email": "galit@gmail.com", "password": "222", "nickname": "galiti"}
        ]

        users = [User(**user_details) for user_details in users]
        for user in users:
            cls._insert_user(user)

    @classmethod
    def _insert_user(cls, user: User) -> int:
        return dbManager.commit(cls._INSERT_USER_SQL, (user.email, user.name, user.nickname, user.password))

    @classmethod
    def get_all_users(cls) -> List[User]:
        raw_users_details = dbManager.fetch(cls._GET_ALL_USERS_SQL)
        if not raw_users_details:
            raise Exception('Failed fetching users')

        return [User(name=d.name, email=d.email, password=d.password, nickname=d.nickname) for d in raw_users_details]

    @classmethod
    def register_user(cls, name: str, email: str, password: str, nickname: str) -> bool:
        user = User(name=name, email=email, password=password, nickname=nickname)
        if not user.is_valid():
            return False

        num_inserted = cls._insert_user(user)
        return num_inserted > 0

    @classmethod
    def update_user_details(cls, email: str, name: str = None, nickname: str = None) -> bool:
        assert name or nickname, 'Did not provide any detail to update'
        sql = f"Update users SET "
        values = []
        if name:
            sql = sql + f" name = '{name}', "
            values.append(name)
        if nickname:
            sql = sql + f" nickname ='{nickname}' "
            values.append(nickname)
        sql = sql + f" WHERE email= '{email}';"
        values.append(email)

        num_rows_updated = dbManager.commit(sql)
        return num_rows_updated > 0

    def delete_user(self, email: str) -> bool:
        rows_affected = dbManager.commit(self._DELETE_USER_SQL % email)
        return rows_affected > 0


    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:
        raw_users_details = dbManager.fetch(cls._GET_USER_BY_ID_SQL, (user_id, ))
        if isinstance(raw_users_details, bool) and not raw_users_details:
            raise Exception('Failed fetching user')
        if not raw_users_details:
            raise UserNotFoundError(f'User {user_id} not found')

        user_data = raw_users_details[0]
        return User(name=user_data.name, email=user_data.email, password=user_data.password, nickname=user_data.nickname)



users_management = UsersManagement()

