import json

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from excercise10.utilities.session_helper import SessionHelper
from excercise10.utilities.users_management import users_management

# assignment10 blueprint definition
assignment10 = Blueprint('assignment10', __name__, static_folder='../../static', static_url_path='/assignment10', template_folder='templates')


# Routes
@assignment10.route('/')
@assignment10.route('/users')
@assignment10.route('/assignment10')
def users():
    users_result = users_management.get_all_users()
    return render_template('assignment10.html', users=[{"name": u.name, "email": u.email, "nickname": u.nickname} for u in users_result])


@assignment10.route('/user', methods=['POST', 'DELETE', 'PUT'])
def user():
    email = request.form.get('email')
    if not email:
        return render_template('assignment10.html', bad_request=True)

    SessionHelper.clear_session_results()

    http_method = request.form.get('_method') or request.method
    if http_method == 'PUT':
        new_name = request.form.get('new_name')
        new_nickname = request.form.get('new_nickname')
        updated_successfully = users_management.update_user_details(email, name=new_name, nickname=new_nickname)
        SessionHelper.set_result_in_session(is_success=updated_successfully, message='update user')
        return redirect(url_for('.users'))
    elif http_method == 'DELETE':
        deleted_successfully = users_management.delete_user(email)
        SessionHelper.set_result_in_session(is_success=deleted_successfully, message='delete user')
        return redirect(url_for('.users'))
    elif http_method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        registered_successfully = users_management.register_user(email=email, name=name, password=password, nickname=nickname)
        SessionHelper.set_result_in_session(is_success=registered_successfully, message='register user')
        return redirect(url_for('.users'))

