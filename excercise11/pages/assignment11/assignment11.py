import requests as requests
from flask import Blueprint, render_template, jsonify, request, url_for
from excercise11.utilities.users_management import users_management

# assignment11 blueprint definition
from excercise11.utilities.session_helper import SessionHelper

assignment11 = Blueprint('assignment11', __name__, static_folder='../../static', static_url_path='/assignment11', template_folder='templates')


# Routes


@assignment11.route('/')
@assignment11.route('/assignment11')
def home():
    return render_template('assignment11.html')


@assignment11.route('/users')
def users():
    users_result = users_management.get_all_users()
    return jsonify(users=[{"name": u.name, "email": u.email, "nickname": u.nickname} for u in users_result])


@assignment11.route('/outer_source')
def outer_source():
    user_id = request.args.get('userId')
    if not user_id:
        SessionHelper.set_result_in_session(is_success=False, message='Did not provide user id')
        return render_template(url_for('.home'))

    url = f'https://reqres.in/api/users/{user_id}'

    try:
        response = requests.get(url)
        user = response.json()["data"]
        return render_template('assignment11.html', user=user)
    except Exception as e:
        SessionHelper.set_result_in_session(is_success=False, message='Failed fetching user from reqres.in')
        print('Failed fetching user', str(e))

    return render_template(url_for('.home'))

