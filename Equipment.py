from Entity import Player
class Equipment:
    def __init__(self, _Type: str, _ID: int, _Name: str, _MaxHP: int,_ATK: int, _DEF: int, _SPD: int, _description: str, _hasPassive: bool,_passiveOnPlayer:bool) -> None:
        self.Type = _Type
        self.ID = _ID
        self.Name = _Name
        self.MaxHP = _MaxHP
        self.ATK = _ATK
        self.DEF = _DEF
        self.SPD = _SPD
        self.description = _description
        self.hasPassive = _hasPassive
        self.passiveOnPlayer = _passiveOnPlayer

    def equipItem(self, player: Player) -> Player:
        player.equipmentStats["MaxHP"] += self.MaxHP
        player.equipmentStats["ATK"] += self.ATK
        player.equipmentStats["DEF"] += self.DEF
        player.equipmentStats["SPD"] += self.SPD
        return player
    
    def unequipItem(self, player: Player) -> Player:
        player.equipmentStats["MaxHP"] -= self.MaxHP
        player.equipmentStats["ATK"] -= self.ATK
        player.equipmentStats["DEF"] -= self.DEF
        player.equipmentStats["SPD"] -= self.SPD
        return player

class Armor(Equipment):
    def __init__(self, _bodyPart: int, _ID: int, _Name: str, _MaxHP: int, _DEF: int, _SPD: int, _description: str, _hasPassive: bool = False, _passiveOnPlayer: bool = False) -> None:
        super.__init__("Armor", _ID, _Name, _MaxHP , 0, _DEF, _SPD, _description, _hasPassive, _passiveOnPlayer)
        self.bodyPart = _bodyPart
    
    def passiveAbility(self)-> None:
        pass

class Weapon(Equipment):
    def __init__(self, _ID: int, _Name: str, _ATK: int, _description: str) -> None:
        super.__init__("Weapon", _ID, _Name, 0, _ATK, 0, 0, _description)

    def passiveAbility(self)-> None:
        pass
