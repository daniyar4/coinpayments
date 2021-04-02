from urllib import parse
from config import merchant_id
from models import SavingTransactions
from app import db
import hashlib
import hmac


class Process:
    """Проверка платежа
    Если платеж нужно отплатить, возвращает True,
    иначе строку с пояснением"""
    def __init__(self, dict_res):
        self.dict_res = dict_res
        self.ipn_version = dict_res["ipn_version"][0]
        self.ipn_id = dict_res["ipn_id"][0]
        self.ipn_mode = dict_res["ipn_mode"][0]
        self.merchant = dict_res["merchant"][0]
        self.txn_id = dict_res["txn_id"][0]
        self.status = dict_res["status"][0]
        self.email = dict_res['email'][0]
        self.status_text = dict_res['status_text'][0]
        self.currency2 = dict_res['currency2'][0]
        self.amount2 = dict_res['amount2'][0]

    def check_merchant(self, my_merchant_id=merchant_id):
        if self.merchant == my_merchant_id:
            return True
        else:
            return False

    def check_payment(self):
        if self.txn_id in SavingTransactions.query.filter(SavingTransactions.txn_id==self.txn_id):
            return False
        else:
            return True

    def check_status(self):
        int_stat = int(self.status)
        if int_stat >= 100:
            return True
        elif 0 < int_stat < 100:
            return False
        else:
            return False

    def main_check(self):
        if self.check_merchant() and self.check_payment() and self.check_status():
            return True
        elif not self.check_payment():
            return 'Уже оплачено'
        elif not self.check_merchant():
            return 'Мерчант ид не совпадает'
        else:
            return self.status_text


def pay(r,ipn_key ):
    """Проверяет ключ hmac, создает экземпляр класса Process и сохраняет в БД
    возвращает dict с данными, ели нужно оплатить"""
    received_hmac = r.headers['Hmac']
    hmac_key = bytearray(ipn_key, 'utf-8')
    generated_hmac = hmac.new(key=hmac_key,
                              msg=r.get_data(),
                              digestmod=hashlib.sha512).hexdigest()
    if received_hmac == generated_hmac:
        res = r.get_data().decode('utf-8')
        dict_res = dict(parse.parse_qs(res))
        processing = Process(dict_res)
        check_result =processing.main_check()
        if check_result == True:
            save = SavingTransactions(
                ipn_version=dict_res["ipn_version"][0],
                ipn_mode=dict_res["ipn_mode"][0],
                merchant_id=dict_res["merchant"][0],
                txn_id = dict_res["txn_id"][0],
                status = dict_res["status"][0],
                email=dict_res['email'][0],
                status_text=dict_res['status_text'][0],
                currency2=dict_res['currency2'][0],
                amount2=dict_res['amount2'][0]
            )
            db.session.add(save)
            db.session.commit()
            return dict_res
        else:
            return 'Платеж не прошел проверку'