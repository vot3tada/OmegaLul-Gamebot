import json
from json import load, dumps
import Classes.Player as Player
from Classes.Good import Good
import Classes.Item as Item

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player.Player):
            return obj.__dict__
        if isinstance(obj, Good):
            return {'id': obj.id}
        return json.JSONEncoder.default(self, obj)
    
class Decoder(json.JSONDecoder):
    def __init__(self, object_hook=None, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if not o.get('userId') is None:
            decoded = Player.Player(
                o.get('userId'), 
                o.get('name'), 
                o.get('photo'),
                o.get('exp'),
                o.get('money'),
                o.get('inventory'),
                o.get('luck'),
                o.get('luckMultiply'),
                o.get('hp'),
                o.get('damage'),
                o.get('damageMultyply'),
                o.get('status')
            )
        elif not o.get('id') is None:
            decoded = Item.Items[o.get('id')]
        return decoded
    
def LoadUsers() -> list[Player.Player]:
    return load(open("users.json","r"), cls=Decoder)

def SaveUsers():
    with open("users.json", "w") as file:
        file.write(dumps(Player.Players, cls=Encoder))
