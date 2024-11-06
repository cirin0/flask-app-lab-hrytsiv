from flask import flash, make_response, render_template, request, redirect, session, url_for
from . import user_bp
from datetime import timedelta


@user_bp.route('/hi/<string:name>')
def greeting(name):
    name = name.upper()
    age = request.args.get('age', 0, int)
    return render_template('users/hi.html', name=name, age=age)


@user_bp.route('/admin')
def admin():
    to_url = url_for("users.greeting", age=45,
                     name='administrator', external=True)
    print(to_url)
    return redirect(to_url)


@user_bp.route('/profile')
def get_profile():
    if 'username' in session:
        username_value = session['username']
        theme = request.cookies.get('theme', 'light')
        return render_template('users/profile.html',
                               username=username_value,
                               cookies=request.cookies,
                               theme=theme)
    flash('Invalid name or password', 'danger')

    return redirect(url_for('users.login'))


@user_bp.route('set_theme/<theme>', methods=['GET'])
def set_theme(theme):
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color', theme, max_age=timedelta(days=30))
    flash(f'Колір теми змінено на {theme}', 'info')
    return response


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    correct_username = "Ivan"
    correct_password = "12345"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == correct_username and password == correct_password:
            session['username'] = username
            flash('You are successfully logged in', 'success')
        return redirect(url_for('users.get_profile'))
    if 'username' in session:
        flash('You are already logged in', 'info')
        return redirect(url_for('users.get_profile'))
    return render_template('users/login.html')


@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('users.get_profile'))


@user_bp.route('/set_cookie', methods=['GET', 'POST'])
def set_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    expiry = request.form.get('expiry')
    if not key or not value or not expiry:
        flash('Будь ласка, заповніть всі поля форми.', 'danger')
        return redirect(url_for('users.get_profile'))

    flash(f'Кука {key} зі значенням {value} створена', 'info')
    response = response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(key, value, max_age=int(expiry))
    return response


@user_bp.route('/get_cookie', methods=['GET', 'POST'])
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'


@user_bp.route('/delete_cookie', methods=['GET', 'POST'])
def delete_cookie():
    delete_key = request.form.get('delete_key')
    flash(f'Кука {delete_key} видалена', 'info')
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(delete_key, '', expires=0)
    return response


@user_bp.route('/delete_all_cookies', methods=['GET', 'POST'])
def delete_all_cookies():
    flash('Всі куки видалені', 'info')
    response = make_response(redirect(url_for('users.get_profile')))
    response.delete_cookie('username')
    response.delete_cookie('color')
    return response
