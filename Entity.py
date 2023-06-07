import math,textwrap,random
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
    
    def updateFinalStats(self) -> None:
        self.finalStats["HP"] = self.HP + self.equipmentStats["MaxHP"]
        self.finalStats["MaxHP"] = self.MaxHP + self.equipmentStats["MaxHP"]
        self.finalStats["ATK"] = self.ATK + self.equipmentStats["ATK"]
        self.finalStats["DEF"] = self.DEF + self.equipmentStats["DEF"]
        self.finalStats["SPD"] = self.SPD + self.equipmentStats["SPD"]

    def calculateDamage(self, damage) -> int:
        finalDamage = super().calculateDamage(damage, self.finalStats["DEF"])
        self.finalStats["HP"] -= finalDamage

        if self.finalStats["HP"] <= 0:
            self.isAlive = False
        return finalDamage
    
    def equipItem(self,equipment) :
        if type(equipment) == Weapon:
            equipmentPart = "Weapon"
            self.equipment[equipmentPart] = equipment
        else:
            equipmentPart = equipment.bodyPart
            self.equipment[equipmentPart] = equipment
        self.equipmentStats["MaxHP"] += self.equipment[equipmentPart].MaxHP
        self.equipmentStats["ATK"] += self.equipment[equipmentPart].ATK
        self.equipmentStats["DEF"] += self.equipment[equipmentPart].DEF
        self.equipmentStats["SPD"] += self.equipment[equipmentPart].SPD
    
    def unequipItem(self,equipment) :
        if type(equipment) == Weapon:
            equipmentPart = "Weapon"
        else:
            equipmentPart = equipment.bodyPart
        self.equipmentStats["MaxHP"] -= self.equipment[equipmentPart].MaxHP
        self.equipmentStats["ATK"] -= self.equipment[equipmentPart].ATK
        self.equipmentStats["DEF"] -= self.equipment[equipmentPart].DEF
        self.equipmentStats["SPD"] -= self.equipment[equipmentPart].SPD
    
    def printStats(self) -> None:
        print(textwrap.dedent(f"""\
        Type = {self.Type}
        Name = {self.Name}
        Health = {self.finalStats["HP"]}
        Max Health = {self.finalStats["MaxHP"]}
        Attack = {self.finalStats["ATK"]}
        Defense = {self.finalStats["DEF"]}
        Speed = {self.finalStats["SPD"]}"""))

