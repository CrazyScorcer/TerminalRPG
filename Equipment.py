from Entity import Player
import sqlite3
class Equipment:
    def __init__(self, _Type: str, _ID: int, _MaxHP: int,_ATK: int, _DEF: int, _SPD: int, _description: str) -> None:
        self.Type = _Type
        self.ID = _ID
        self.MaxHP = _MaxHP
        self.ATK = _ATK
        self.DEF = _DEF
        self.SPD = _SPD
        self.description = _description

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
    
    def updateDB(self, player:Player, bodyPart: str = "") -> None:
        connection = sqlite3.connect("Info.db")
        cursor = connection.cursor()

        if self.Type == "Armor":
            playerArmorExist = cursor.execute(f"Select Count() From ((PlayerArmor Inner Join Armor On PlayerArmor.ArmorID = Armor.ArmorID) Inner Join ArmorType ON Armor.ArmorTypeID = ArmorType.ArmorTypeID) Where PlayerArmor.PlayerName = {player.Name} And ArmorType.Name = {bodyPart}").fetchone()[0]
            if playerArmorExist:
                cursor.execute(f"Delete PlayerArmor Where PlayerName = {player.Name} And Armor.ID = {self.ID})")
            cursor.execute(f"Insert Into PlayerArmor Values({player.Name},{self.ID})")
        else:
            playerWeaponExist = cursor.execute(f"Select Count(PlayerName) From PlayerWeapon Where PlayerName = {player.Name}").fetchone()[0]
            if playerWeaponExist:
                cursor.execute(f"Delete PlayerWeapon Where PlayerName = {player.Name})")          
            cursor.execute(f"Insert Into PlayerWeapon Values({player.Name},{self.ID})")
        
        connection.commit()
        connection.close()

class Armor(Equipment):
    def __init__(self, _bodyPart: str, _MaxHP: int, _DEF: int, _SPD: int, _description: str) -> None:
        super.__init__("Armor",_MaxHP,0,_DEF,_SPD,_description)
        self.bodyPart = _bodyPart
    
    def updateDB(self, player: Player) -> None:
        super().updateDB(player, self.bodyPart)

class Weapon(Equipment):
    def __init__(self, _ATK: int, _description: str) -> None:
        super.__init__("Weapon",0,_ATK,0,0,_description)


        
