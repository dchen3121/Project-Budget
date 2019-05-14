import os
from flask import Flask, render_template, redirect, url_for
from views.stores import store_blueprint
from views.alerts import alert_blueprint
from views.users import user_blueprint
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "s7@8ob3fn8$%9nf64o&bv02q84gn74v!o78o34u78#27g4fno49lu*7h87q23fb1ui"
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)
load_dotenv()

app.register_blueprint(alert_blueprint, url_prefix="/alerts")  # registering alert_blueprint, setting prefix url
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")


@app.route('/')
def home():
    return redirect(url_for('users.login_user'))


if __name__ == '__main__':
    app.run(debug=True)
