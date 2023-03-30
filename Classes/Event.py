from datetime import datetime, date, time

class Event():
    name = ''
    datetime = datetime.today()
    players = []
    
    
    def __init__(self):
        self.datetime = datetime.today()
        self.players = []


a = f'{datetime(2005, 7, 14, 12, 30):%Y-%m-%d-%H-%M}'
print(a)