from flask import Blueprint, render_template, redirect, url_for, session, request
from models.personal.spending import Spending
from models.user import requires_login
from common.utils import Utils

spendings_blueprint = Blueprint('spendings', __name__)


@spendings_blueprint.route('/')
@requires_login
def index():
    spendings = Spending.find_sorted_descending({'user_email': session['email']}, 'date')
    return render_template('spendings/index.html', spendings=spendings)


@spendings_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_spending():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        price = float(request.form['price'])
        date = request.form['date']
        if "income" == request.form['radioIO']:
            is_expense = False
        else:
            is_expense = True
        if len(date) == 10:
            spending = Spending(title, category, price, session['email'], is_expense, date=date)
        else:
            spending = Spending(title, category, price, session['email'], is_expense)
        spending.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('spendings/new_spending.html')


@spendings_blueprint.route('/edit/<string:spending_id>', methods=['GET', 'POST'])
@requires_login
def edit_spending(spending_id):
    spending = Spending.get_by_id(spending_id)
    if request.method == 'POST':
        new_title = request.form['title']
        new_category = request.form['category']
        new_price = request.form['price']
        new_date = request.form['date']
        if "income" == request.form['radioIO']:
            is_expense = False
        else:
            is_expense = True
        spending.title = new_title
        spending.category = new_category
        spending.price = new_price
        spending.date = new_date
        spending.is_expense = is_expense
        spending.save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('spendings/edit_spending.html', spending=spending)


@spendings_blueprint.route('/delete/<string:spending_id>')
@requires_login
def delete_spending(spending_id):
    spending = Spending.get_by_id(spending_id)
    if spending.user_email == session['email']:
        spending.remove_from_mongo()
    return redirect(url_for('.index'))


@spendings_blueprint.route('/sort/<string:sort_by>_<string:asc>')
@requires_login
def sort(sort_by, asc):
    if asc == "True":
        spendings = Spending.find_sorted_descending({'user_email': session['email']}, sort_by)
    else:
        spendings = Spending.find_sorted_ascending({'user_email': session['email']}, sort_by)
    return render_template('spendings/index.html', spendings=spendings)
