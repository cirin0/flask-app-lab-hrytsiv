from flask import flash, make_response, render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app.users.forms import RegistrationForm, LoginForm
from . import user_bp
from datetime import timedelta

from app.users.models import User
from app import db
from app import login_manager


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('users.get_account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User(username=form.username.data, email=email)
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form, title='Register')


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
@login_required
def get_profile():
    if 'username' in session:
        username_value = session['username']
        theme = request.cookies.get('theme', 'light')
        return render_template('users/profile.html',
                               username=username_value,
                               cookies=request.cookies,
                               theme=theme)
    flash('Please log in', 'info')
    return redirect(url_for('users.login'))


@user_bp.route('set_theme/<theme>', methods=['GET'])
def set_theme(theme):
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color', theme, max_age=timedelta(days=30))
    flash(f'Колір теми змінено на {theme}', 'info')
    return response


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('users.get_account'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You are successfully logged in', 'success')
            return redirect(url_for('users.get_account'))
        flash('Invalid email or password', 'danger')
    return render_template('users/login.html', form=form, title='Login')


@user_bp.route('/account')
@login_required
def get_account():
    all_users = User.query.all()
    user_count = len(all_users)
    return render_template('users/account.html', user=current_user, all_users=all_users, count=user_count)


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('users.login'))


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
