api_url = 'https://www.coinpayments.net/api.php'
open_key = 'your open key'
private_key = 'your privat private_key'
merchant_id = 'your merchant_id'
ipn_key = 'your ipn'


class Configuration:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coinpayments.db'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False