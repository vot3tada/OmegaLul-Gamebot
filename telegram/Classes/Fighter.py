from typing import Any
import Classes.Player as Player
HPCut : int = 10
UltaCharge: int = 4

fighter = {
    'health':100,
    'luck':0.2,
    'damage':25,
    'rageFactor':0,
    'dexFactor': 0,
    'defence': 1,
    'ulta': 0,
    'charge': 0
}

def ExpReward(hp: int) -> int:
    return 50 + 100 * (100 - hp)//(100)

def MoneyReward(hp: int) -> int:
    return 10 + 25 * (100 - hp)//(100)

fight_texts = [
    'Каждую пятницу одно и тоже!\n',
    'Заходи! Сбоку заходи!\n',
    'Кранты вам всем!!\n',
    'Ааа, ща мы вам, арабы недоделанные!\n',
    'Выноси бычьё!\n'
]

def getFighterData(player: Player.Player) -> dict[str, Any]:
    level = player.level
    fighterData = fighter.copy()
    fighterData['health'] = player.hp
    fighterData['luck'] = (player.luck + Player.levelLuckFactor * level) * player.luckMultiply
    fighterData['damage']= (player.damage + Player.levelDamageFactor * level) * player.damageMultiply
    return fighterData