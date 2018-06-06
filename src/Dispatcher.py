from sinchsms import SinchSMS
from config import SinchConfig as sc
import threading

class Dispatcher:

    SN_KEY = None
    SN_SEC = None
    client = None
    
    message_queue = {}
    confirmation_queue = []

    def __init__(self):
        self.SN_KEY = sc.key
        self.SN_SEC = sc.secret
        self.client = SinchSMS(self.SN_KEY, self.SN_SEC)
        threading.Timer(6, self.confirm).start()

    def queue(self, message, number):
        if not number in self.message_queue:
            self.message_queue[number] = [message]
        else:
            if message in self.message_queue[number]:
                raise ValueError("Queueing the same message to a number more than once is not allowed!")
            if message == "":
                raise ValueError("Queueing empty messages is not allowed!")
            self.message_queue[number].append(message)
        return True 
        
    def dispatch(self, callback = None):
        dispatch_count = 0
        for number in self.message_queue:
            grouped_message = ""
            for message in self.message_queue[number]:
                grouped_message += "{0}\n".format(message)
            response = self.client.send_message(number, grouped_message)
            dispatch_count += 1
            message_entity = {
                'receiver': number,
                'text': grouped_message,
                'id': response['messageId'],
                'ttl': 10
            }
            self.confirmation_queue.append(message_entity)
        self.message_queue = {}
        if callback: callback({'dispatched': dispatch_count})
            
    
    def confirm(self):
        unconfirmed = []
        if not self.confirmation_queue == None:
            for msg in self.confirmation_queue:
                status = self.client.check_status(msg['id'])
                if not status == 'Successful':
                    msg['ttl'] -= 1
                    if msg['ttl'] == 0:
                        raise TimeoutError("Could not send message to {nr}! Confirmation timeout\nContent: {text}".format(nr=msg['receiver'], text=msg['text']))
                    unconfirmed.append(msg)
                else:
                    msg['callback']({'receiver': msg['receiver'], 'message': msg['text']})
            self.confirmation_queue = unconfirmed


  
