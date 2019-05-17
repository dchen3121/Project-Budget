from flask import Blueprint, render_template, request, redirect, url_for, session
from models.pricing.alert import Alert
from models.pricing.store import Store
from models.pricing.item import Item
from models.user.decorators import requires_login
from common.utils import Utils


alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@requires_login
def index():
    alerts = Alert.find_sorted_descending({'user_email': session['email']}, "below_limit")
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        # process the data from form
        item_name = request.form['item_name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()

        date_entered = Utils.get_date_accurate()

        alert = Alert(date_entered, item._id, price_limit, item_name, session['email'], 0)
        Alert.load_item_price(alert)
        alert.item.save_to_mongo()
        alert.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    """
    If method is GET:
      Takes user to the edit alert page
      User makes changes and confirms, then creates POST onto same endpoint
    If method is POST:
      Redirects user to the index homepage with the info all updated
    :param alert_id: used to get the alert object from the database
    """
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        new_item_name = request.form['item_name']
        new_price_limit = float(request.form['price_limit'])

        alert.item_name = new_item_name
        alert.price_limit = new_price_limit

        Alert.load_item_price(alert)
        alert.item.save_to_mongo()
        alert.save_to_mongo()

        return redirect(url_for('.index'))  # the '.' means the current blueprint, 'index' is the name of function
    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/sort/<string:sort_by>_<string:asc>')
@requires_login
def sort_alerts(sort_by, asc):
    if asc == "True":
        alerts = Alert.find_sorted_descending({'user_email': session['email']}, sort_by)
    else:
        alerts = Alert.find_sorted_ascending({'user_email': session['email']}, sort_by)
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))

