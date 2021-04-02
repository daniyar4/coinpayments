import hashlib
import hmac
import urllib.error
import urllib.parse
import urllib.request
import time
import requests

from config import private_key, api_url, open_key


def create_hmac(p):
    encoded = urllib.parse.urlencode(p).encode('utf-8')
    hmac_private = bytearray(private_key, 'utf-8')
    hmac_params = hmac.new(hmac_private, encoded, hashlib.sha512)
    hmac_sign = encoded, hmac_params.hexdigest()
    return hmac_sign


def get_rates():
    """Gets current rates for currencies
       https://www.coinpayments.net/apidoc-rates
    """
    params = {'format': 'json',
              'version': 1,
              'cmd': 'rates',
              'key': open_key,
              }
    encoded, sig = create_hmac(params)
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'hmac': sig,
               }
    currencies_rates = requests.post(api_url, data=encoded, headers=headers)
    return currencies_rates.json()


class MakeCoinsList:
    """Creating a list of cryptocurrencies
       for the deposit button every 60 seconds
     """
    def __init__(self, rates):
        self.coins_list = []
        self.update_time = 0

    def make_coins_list(self, rates):
        time_difference = time.time() - self.update_time
        print(time_difference)
        if time_difference > 60.0:
            self.update_time = time.time()
            self.coins_list = []
            currencies_rates = rates()
            for coin in currencies_rates['result']:
                if 'payments' in currencies_rates['result'][coin]['capabilities']:
                    self.coins_list.append(coin)
        return self.coins_list
