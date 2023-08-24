# Special file to create custom passive to Armor
from Equipment import Armor
from Entity import Monster
from enum import Enum
class ArmorType(Enum):
    Helmet = 1
    Chestplate = 2
    Leggings = 3
    Footwear = 4

class BasicHelmet(Armor):
    def __init__() -> None:
        super().__init__(Enum('Helmet'), 1, 'BasicHelmet', 0, 2, 0, 'A basic Helmet')

class SpikeHelmet(Armor):
    def __init__() -> None:
        super().__init__(Enum('Helmet'), 2, 'SpikeHelm', 0, 1, 0, 'When attacked by an enemy, the enemy takes 1 damage', True, True)

    def passiveAbility(self, monsterObject:Monster) -> None:
        monsterObject.HP -= 1
        return super().passiveAbility()