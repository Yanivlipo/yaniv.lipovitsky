import uuid

from flask import Flask, redirect, render_template, request, session
import users_management

app = Flask(__name__)

app.secret_key = str(uuid.uuid4())


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/')
def home():
    return redirect('/cv')


@app.route('/assignment9')
def assignment9():
    return render_template('assignment9.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        search_value = request.args.get('search')
        if not search_value:
            users_result = users_management.get_all_users()
        else:
            users_result = users_management.get_user(search_value)
        if not users_result:
            return render_template('assignment9.html', not_found=True)
        return render_template('assignment9.html', users=[{"name": u.name, "email": u.email} for u in users_result])
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        user = users_management.register_user(name=name, email=email, password=password, nickname=nickname)
        session['user'] = user
        return render_template('assignment9.html', failed_registered=user is None)


@app.route('/logout')
def logout():
    session['user'] = None
    return render_template('/assignment9.html')


if __name__ == '__main__':
    app.run(debug=True)
