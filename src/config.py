class SinchConfig:
   key = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   secret = "xxxxxxxxxx"


class NotificationConfig:
    interval = 180
    default_sleep = {'begin': 21, 'end': 7}
    margin_percent = 5
    margin_timespan = 60 * 24
    margins_fixed = {
        'low': [5000, 6000],
        'high': [7500, 9500]
    }

class ExchangeConfig:
    coinbase = {
        'url': 'https://api.coinbase.com/v2/prices/BTC-{currency}/{type}',
        'currency': 'EUR'
    }
    kraken = {}


class Users:
    userlist = {
        1 : {
            'name': 'main',
            'number': 'xxxxxxxxxxxx',
            'receive_default': True,
            'receive_critical': True
        }
    }

