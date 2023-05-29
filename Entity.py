import math,textwrap,random

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

    def calculateDamage(self,damage) -> int:
        damage = damage*math.pow(math.e,(-self.DEF/damage))
        if self.isDefending:
            damage = damage/2

        finalDamage = round(damage) if round(damage) > 1 else 1
        self.HP -= finalDamage

        if self.HP <= 0:
            self.isAlive = False

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

class Player(Entity):
    def __init__(self,_playerName: str,_playerStatsDict: dict,_playerJob: int,_playerLVLStats: tuple) -> None:
        super().__init__("Player",_playerName,_playerStatsDict)
        self.playerJob = _playerJob
        self.playerLVLStats = _playerLVLStats
        self.equipment = {
            "Helmet" : None,
            "Chestplate" : None,
            "Leggings" : None,
            "Footwear" : None,
            "Weapon": None
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

