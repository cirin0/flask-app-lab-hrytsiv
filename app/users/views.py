from flask import make_response, render_template, request, redirect, url_for
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


@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука установлена')
    response.set_cookie('username', 'student',
                        max_age=timedelta(seconds=60).total_seconds())
    response.set_cookie('color', 'black',
                        max_age=timedelta(seconds=60).total_seconds())
    return response


@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'


@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0)
    return response
