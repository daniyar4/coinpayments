
from CoinPayments import MakeCoinsList, get_rates
from app import app
from flask import render_template, request
from config import merchant_id, ipn_key
from ipn_model import pay

coins = MakeCoinsList(get_rates)


@app.route('/')
def index():
    button_data = {
        'merchant': merchant_id,
        'cmd': '_cart_add',
    }
    return render_template('index.html', button_data=button_data,
                           coins_list=coins.make_coins_list(get_rates))


@app.route("/ipn/", methods=["POST"])
def ipn():
    r = request
    pay(r, ipn_key)
    return "ok"
