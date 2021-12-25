import dataclasses
import json
import pathlib

_USERS_FILENAME = pathlib.Path(pathlib.Path(__file__).parent.resolve(), 'users.json')


@dataclasses.dataclass
class User:
    name: str
    email: str
    password: str
    nickname: str

    def is_valid(self):
        return self.name and self.email and self.password and self.nickname


_USERS = [User(**user_data) for user_data in json.loads(_USERS_FILENAME.read_text()).get('users').values()]


def get_all_users():
    return _USERS


def get_user(search_value: str):
    matching_users = [u for u in _USERS if u.name.lower() == search_value.lower() or u.email.lower() == search_value.lower()]

    if not matching_users:
        return None
    return matching_users


def register_user(name: str, email: str, password: str, nickname: str):
    user = User(name=name, email=email, password=password, nickname=nickname)
    if not user.is_valid():
        return None

    _USERS.append(user)
    return user
