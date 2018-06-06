from Exchange import Exchange
import requests
from config import ExchangeConfig as conf
import datetime as dt

class Coinbase(Exchange):

    name = "Coinbase"
    endpoint = conf.coinbase['url']

    def get_price(self, _type="spot", _timestamp = dt.datetime.now()):
        url =  self.endpoint.format(currency=self.currency, type=_type)
        dt_str = _timestamp.strftime("%Y-%m-%d %H:%M:%S")
        r = requests.get(url, params={'date':dt_str})
        data = r.json()
        return data['data']['amount']
        
