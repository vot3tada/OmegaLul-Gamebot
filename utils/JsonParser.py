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
        if not o.get('_userId') is None:
            decoded = Player.Player(
                o.get('_userId'), 
                o.get('_name'), 
                o.get('_photo'),
                o.get('_exp'),
                o.get('_money'),
                o.get('_inventory'),
                o.get('_luck'),
                o.get('_luckMultiply'),
                o.get('_hp'),
                o.get('_damage'),
                o.get('_damageMultiply'),
                o.get('_status')
            )
        elif not o.get('id') is None:
            decoded = Item.Items[o.get('id')]
        return decoded
    
def LoadUsers() -> list[Player.Player]:
    return load(open("users.json","r"), cls=Decoder)

#{"userId": "546270371_546270371", "name": "\u0410\u0431\u043e\u0431\u0430", "exp": 0, "money": 350, "photo": "./static/546270371_546270371.jpg", "inventory": [{"id": "LuckPotion"}, {"id": "DamagePotion"}, {"id": "HPPotion"}, {"id": "HPPotion"}, {"id": "HPPotion"}, {"id": "HPPotion"}], "luck": 0.2, "luckMultiply": 1, "hp": 50, "damage": 20, "damageMultiply": null, "status": []}

def SaveUsers():
    with open("users.json", "w") as file:
        file.write(dumps(Player.Players, cls=Encoder))
