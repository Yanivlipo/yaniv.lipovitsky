import http

import requests as requests
from flask import Blueprint, render_template, jsonify, request, url_for
from excercise12.utilities.users_management import users_management, UserNotFoundError

# assignment12 blueprint definition
from excercise12.utilities.session_helper import SessionHelper

assignment12 = Blueprint('assignment12', __name__, static_folder='../../static', static_url_path='/assignment12', template_folder='templates')


# Routes


@assignment12.route('/')
@assignment12.route('/assignment12')
def home():
    return render_template('assignment12.html')


@assignment12.route('/users')
def users():
    users_result = users_management.get_all_users()
    return jsonify(users=[{"name": u.name, "email": u.email, "nickname": u.nickname} for u in users_result])


@assignment12.route('/outer_source')
def outer_source():
    user_id = request.args.get('userId')
    if not user_id:
        SessionHelper.set_result_in_session(is_success=False, message='Did not provide user id')
        return render_template(url_for('.home'))

    url = f'https://reqres.in/api/users/{user_id}'

    try:
        response = requests.get(url)
        user_data = response.json()["data"]
        return render_template('assignment12.html', user=user_data)
    except Exception as e:
        SessionHelper.set_result_in_session(is_success=False, message='Failed fetching user from reqres.in')
        print('Failed fetching user', str(e))

    return render_template(url_for('.home'))


@assignment12.route('/assignment12/restapi_users', defaults={"user_id": users_management.DEFAULT_USER_ID})
@assignment12.route('/assignment12/restapi_users/<int:user_id>')
def user(user_id: int):
    try:
        user_data = users_management.get_user_by_id(user_id=user_id)
        return jsonify(user={"name": user_data.name, "email": user_data.email, "nickname": user_data.nickname})
    except UserNotFoundError:
        return jsonify(dict(error=True, status=http.HTTPStatus.NOT_FOUND, message="Did not find user with this id", user_id=user_id))
    except Exception:
        return jsonify(dict(error=True, status=http.HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed fetching user", user_id=user_id))