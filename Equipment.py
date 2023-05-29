from Entity import Player
class Equipment:
    def __init__(self, _Type: str, _MaxHP: int,_ATK: int, _DEF: int, _SPD: int) -> None:
        self.Type = _Type
        self.MaxHP = _MaxHP
        self.ATK = _ATK
        self.DEF = _DEF
        self.SPD = _SPD
    
    def equipItem(self, player: Player) -> Player:
        player.HP += self.MaxHP
        player.MaxHP += self.MaxHP
        player.ATK += self.ATK
        player.DEF += self.DEF
        player.SPD += self.SPD
        return player
    
    def unequipItem(self, player: Player) -> Player:
        player.HP -= self.MaxHP
        if player.HP < 1:
            player.HP = 1
        player.MaxHP -= self.MaxHP
        player.ATK -= self.ATK
        player.DEF -= self.DEF
        player.SPD -= self.SPD
        return player

class Armor(Equipment):
    def __init__(self, _MaxHP: int, _DEF: int, _SPD: int) -> None:
        super.__init__("Armor",_MaxHP,0,_DEF,_SPD)

class Weapon(Equipment):
    def __init__(self, _ATK: int) -> None:
        super.__init__("Weapon",0,_ATK,0,0)
        
        
