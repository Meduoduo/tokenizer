from threading import Lock, Timer
from requests import get

current_exchange = {
    'CNY': 1,
    'USD': 1 / 6.5,
    'EUR': 1 / 7.5,
    'JPY': 1 / 0.06,
    'GBP': 1 / 8.5,
}
current_exchange_lock = Lock()

def get_exchange_rate(currency):
    with current_exchange_lock:
        return current_exchange[currency]

def set_exchange_rate(currency, rate):
    with current_exchange_lock:
        current_exchange[currency] = rate

def caculate_money(money, from_currency, to_currency):
    with current_exchange_lock:
        ratio = current_exchange[to_currency] / current_exchange[from_currency] 
        return money * ratio

def update_exchange_rate():
    res = get('https://api.exchangerate-api.com/v4/latest/CNY')
    if res.status_code == 200:
        data = res.json()
        with current_exchange_lock:
            for currency, rate in data['rates'].items():
                current_exchange[currency] = rate
    else:
        print('Error: cannot update exchange rate')

def start_update_exchange_rate():
    def update():
        update_exchange_rate()
        Timer(3600, update).start()
    update_exchange_rate()

    thread = Timer(3600, update)
    thread.start()
    print('Exchange rate update thread started.')