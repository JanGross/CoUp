from Dispatcher import Dispatcher
import datetime as dt
from Exchanges.Coinbase import Coinbase
from config import Users, ExchangeConfig
from config import NotificationConfig as ntfc
import time, sys

dispatcher = Dispatcher()
coinbase = Coinbase('cb', ExchangeConfig.coinbase['currency'])

exchanges = [coinbase]
default_countdown = int(sys.argv[1]) if len(sys.argv) > 1 else 60
trigger_reset = 15
highest_triggered = None
lowest_triggered = None
sec_cd = 60

def main_loop(sec_cd):
    sec_cd -= 1
    global default_countdown
    if sec_cd <= 0:
        sec_cd = 60
        hour_now = dt.datetime.now().hour
        if hour_now  >= ntfc.default_sleep['end'] and hour_now <= ntfc.default_sleep['begin']:
            default_countdown -= 1
        else: default_countdown = 1
        update()
    sys.stdout.write("\r{scd}|Next default msg in {cd} min  ".format(scd=sec_cd, cd=default_countdown))
    sys.stdout.flush()
    time.sleep(1)
    return sec_cd

def update():
    global default_countdown
    global trigger_reset
    global highest_triggered
    global lowest_triggered
    global dispatcher
    global coinbase
    global exchanges

    past_ts = dt.datetime.now()-dt.timedelta(minutes=ntfc.margin_timespan)
    for exchange in exchanges:
        current_price = float(exchange.get_price())
        current_buy = float(exchange.get_price(_type="buy"))
        current_sell = float(exchange.get_price(_type="sell"))
        past_price = float(exchange.get_price(_timestamp=past_ts))
        
        difference_percent = abs(current_price - past_price)/current_price

        message_collection = []

        if default_countdown <= 0:
            message_collection.append({
                'text': "Current BTC price on {exchange_name}:{current} \n (Buy {buy}, sell {sell})".format(exchange_name=exchange.name, current=current_price, buy=current_buy, sell=current_sell),
                'category': "default"})
            default_countdown = ntfc.interval
        if difference_percent > ntfc.margin_percent:
                message_collection.append({
                    'text': "Percent margin notification triggered! {sign}{percent} in the last {timespan} minutes. BTC = {current}".format(
                        percent=difference_percent, timespan=ntfc.margin_timespan, current=current_price, sign= '+' if current_price > last_price else '-' ),
                    'category': "critical"})
        for margin in sorted(ntfc.margins_fixed['low']):
            if current_price < margin:
                if not lowest_triggered or lowest_triggered > margin: 
                    lowest_triggered = margin
                    message_collection.append({
                        'text': "Fixed margin reached v({set_margin})! BTC = {current}".format(set_margin=margin, current=current_price), 
                        'category': "critical"})
                
        
        for margin in sorted(ntfc.margins_fixed['high'], reverse=True):
            if current_price >= margin:
                if not highest_triggered or highest_triggered < margin:
                    highest_triggered = margin
                    message_collection.append({
                         'text': "Fixed margin reached ^({set_margin})! BTC = {current}".format(set_margin=margin, current=current_price),
                         'category': "critical"})
    for user_id in Users.userlist:
        ul = Users.userlist
        for message in message_collection:
            if message['category'] == "critical" and ul[user_id]['receive_critical']:
                dispatcher.queue(message['text'], ul[user_id]['number'])
            if message['category'] == "default" and ul[user_id]['receive_default']:
                dispatcher.queue(message['text'], ul[user_id]['number'])
    if trigger_reset <= 0:
        highest_triggered = None
        lowest_triggered = None
        trigger_reset = 15

    dispatcher.dispatch(on_dispatch)

def on_dispatch(result):
    if result['dispatched'] > 0:
        print("\r{0} messages dispatched           ".format(result['dispatched']))

if __name__=='__main__':
    print("CoUp started")
    while True:
        sec_cd = main_loop(sec_cd)
