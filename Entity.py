import math,textwrap,random
import sqlite3

from Equipment import Equipment, Armor, Weapon
class Entity():
    def __init__(self, _Type: str, _Name:str, _statDic: dict) -> None:
        self.Type = _Type 
        self.Name = _Name
        self.LVL = _statDic['LVL']
        self.HP = _statDic['MaxHP']
        self.MaxHP = _statDic['MaxHP']
        self.ATK = _statDic['ATK']
        self.DEF = _statDic['DEF']
        self.SPD = _statDic['SPD']
        
        self.isDefending = False
        self.isAlive = True

    def calculateDamage(self,damage,defense = None) -> int:
        if defense == None:
            defense = self.DEF
        damage = damage*math.pow(math.e,-defense/damage)
        if self.isDefending:
            damage = damage/2

        finalDamage = round(damage) if round(damage) > 1 else 1
        return finalDamage

    def printStats(self) -> None:
        print(textwrap.dedent(f"""\
        Type = {self.Type}
        Name = {self.Name}
        Health = {self.HP}
        Max Health = {self.MaxHP}
        Attack = {self.ATK}
        Defense = {self.DEF}
        Speed = {self.SPD}"""))

class Monster(Entity):
    def __init__(self,_monsterName,_monsterStatsDict) -> None:
        super().__init__("Monster",_monsterName,_monsterStatsDict) 
    
    def randomAction(self) -> str:
        return random.choice(["Attack","Defend"])
    
    def calculateDamage(self, damage) -> int:
        finalDamage = super().calculateDamage(damage)
        self.HP -= finalDamage

        if self.HP <= 0:
            self.isAlive = False
            
        return finalDamage

class Player(Entity):
    def __init__(self,_playerName: str,_playerStatsDict: dict,_playerJob: int,_playerLVLStats: tuple) -> None:
        super().__init__("Player",_playerName,_playerStatsDict)
        self.playerJob = _playerJob
        self.playerLVLStats = _playerLVLStats
        self.equipment: dict[str, Equipment] = {
            "Helmet" : None,
            "Chestplate" : None,
            "Leggings" : None,
            "Footwear" : None,
            "Weapon": None
        }
        self.equipmentStats: dict[str, int] = {
            "MaxHP" : 0,
            "ATK" : 0,
            "DEF" : 0,
            "SPD" : 0
        }
        self.finalStats: dict[str, int] = {
            "HP" : 0,
            "MaxHP" : 0,
            "ATK" : 0,
            "DEF" : 0,
            "SPD" : 0,
        }
        self.EXP = 0
        self.MaxEXP = round(math.pow(math.e,self.LVL/100)*(self.LVL+5))
    
    def checkLVL(self) -> bool:
        if self.EXP < self.MaxEXP:
            return False
        
        self.LVL += 1
        self.EXP -= self.MaxEXP
        self.MaxEXP = round(math.pow(math.e,self.LVL/100)*(self.LVL+5))
        self.eventLVLUP()
        return True
    
    def eventLVLUP(self) -> None:
        self.HP += self.playerLVLStats[0]
        self.MaxHP += self.playerLVLStats[0]
        self.ATK += self.playerLVLStats[1]
        self.DEF += self.playerLVLStats[2]
        self.SPD += self.playerLVLStats[3]

    def equipItem(self, equipmentItem: Equipment) -> None:
        if equipmentItem.Type == 'Armor':
            self.equipment[equipmentItem.bodyPart] = equipmentItem
        else:
            self.equipment['Weapon'] = equipmentItem
        self.equipmentStats["MaxHP"] += equipmentItem.MaxHP
        self.equipmentStats["ATK"] += equipmentItem.ATK
        self.equipmentStats["DEF"] += equipmentItem.DEF
        self.equipmentStats["SPD"] += equipmentItem.SPD
        self.updatePlayerInventoryDB(equipmentItem,True)
    
    def unequipItem(self, equipmentItem: Equipment) -> None:
        if equipmentItem.Type == 'Armor':
            self.equipment[equipmentItem.bodyPart] = None
        else:
            self.equipment['Weapon'] = None
        self.equipmentStats["MaxHP"] -= self.MaxHP
        self.equipmentStats["ATK"] -= self.ATK
        self.equipmentStats["DEF"] -= self.DEF
        self.equipmentStats["SPD"] -= self.SPD
        self.updatePlayerInventoryDB(equipmentItem)

    def updatePlayerInventoryDB(self,equipmentItem: Equipment, addItem: bool = False) -> None:
        connection = sqlite3.connect("Info.db")
        cursor = connection.cursor()

        if self.Type == "Armor":
            #Remove Armor
            playerArmorExist = cursor.execute(f"Select Count() From ((PlayerArmor Inner Join Armor On PlayerArmor.ArmorID = Armor.ArmorID) Inner Join ArmorType ON Armor.ArmorTypeID = ArmorType.ArmorTypeID) Where PlayerArmor.PlayerName = {self.Name} And ArmorType.Name = {equipmentItem.bodyPart}").fetchone()[0]
            if playerArmorExist:
                cursor.execute(f"Delete PlayerArmor Where PlayerName = {self.Name} And Armor.ID = {equipmentItem.ID})")
            #Add Armor
            if addItem:
                cursor.execute(f"Insert Into PlayerArmor Values({self.Name},{equipmentItem.ID})")
        else:
            #Remove Weapon
            playerWeaponExist = cursor.execute(f"Select Count(PlayerName) From PlayerWeapon Where PlayerName = {self.Name}").fetchone()[0]
            if playerWeaponExist:
                cursor.execute(f"Delete PlayerWeapon Where PlayerName = {self.Name})")   
            #Add Weapon
            if addItem:
                cursor.execute(f"Insert Into PlayerWeapon Values({self.Name},{equipmentItem.ID})")
        
        connection.commit()
        connection.close()

    def getAdjustedStats(self) -> dict[int]:
        return {
            "HP" : self.HP + self.equipmentStats["MaxHP"],
            "MaxHP" : self.MaxHP + self.equipmentStats["MaxHP"],
            "ATK" : self.ATK + self.equipmentStats["ATK"],
            "DEF" : self.DEF + self.equipmentStats["DEF"],
            "SPD" : self.SPD + self.equipmentStats["SPD"],
        }
