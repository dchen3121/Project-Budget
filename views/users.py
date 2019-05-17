from flask import request, session, render_template, Blueprint, redirect, url_for, flash
from models.user import User, errors, requires_login
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
            return redirect('/')
        except errors.UserError as e:
            flash(e.message, 'danger')
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
            flash(e.message, 'danger')
    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect('/')


@user_blueprint.route('/settings')
@requires_login
def settings():
    return render_template('users/settings.html')


@user_blueprint.route('/change_password', methods=['POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['current']
        user = User.find_by_email(session['email'])
        current_password_confirm = user.password
        new_password = request.form['new-password']
        new_password_confirm = request.form['new-password-confirm']
        if not Utils.check_hashed_password(current_password, current_password_confirm):
            flash('Incorrect password.', 'danger')
        elif new_password != new_password_confirm:
            flash('The passwords entered do not match.', 'danger')
        else:
            user.password = Utils.hash_password(new_password)
            user.save_to_mongo()
    return redirect(url_for('users.settings'))


@user_blueprint.route('/change_email', methods=['POST'])
def change_email():
    if request.method == 'POST':
        new_email = request.form['new-email']
        new_email_confirm = request.form['new-email-confirm']
        if new_email != new_email_confirm:
            flash('The emails entered do not match.', 'danger')
        else:
            user = User.find_by_email(session['email'])
            user.email = new_email
            session['email'] = new_email
            user.save_to_mongo()
    return redirect(url_for('users.settings'))
