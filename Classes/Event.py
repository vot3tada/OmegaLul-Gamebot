from datetime import datetime, date, time

class Event():
    name = ''
    datetime = datetime.today()
    players = []
    creator = ''
    
    
    def __init__(self):
        self.datetime = datetime.today()
        self.players = []