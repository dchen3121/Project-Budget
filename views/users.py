from flask import request, session, render_template, Blueprint, redirect, url_for
from models.user import User, errors
from common.utils import Utils

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # registering the user
        try:
            User.register_user(email, password)
            session['email'] = email
            return redirect(url_for('/'))
        except errors.UserError as e:
            return e.message
    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect('/')
        except errors.UserError as e:
            return e.message
    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('users.login_user'))
