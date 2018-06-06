class Exchange:

    name = None
    identifier = None
    currency = None
    endpoint = None
    credentials = {}

    def __init__(self, _identifier, _currency, **kwargs):
        self.identifier = _identifier
        self.currency = _currency
        if 'credentials' in kwargs: self.credentials = kwargs['credentials']

    def get_price(self, _type, _timestamp):
        raise NotImplementedError("Get price not implemented for this Exchange")

