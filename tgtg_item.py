class TgtgItem:
    '''Class to represent a single item in the tgtg API
    name: Name of the item
    price: Price of the item
    start_time: Start time to pick up the item
    end_time: End time to pick up the item
    '''

    def __init__(self, api_response: dict) -> None:
        '''Takes the dictionary from the API response and initializes the object
        :param api_response: Dictionary from the API response
        '''
        self.name = api_response['display_name']
        self.price = api_response['item']['price_including_taxes']['minor_units']
        self.start_time = None
        self.end_time = None
        if 'pickup_interval' in api_response.keys():
            self.start_time = api_response['pickup_interval']['start']
            self.end_time = api_response['pickup_interval']['end']
