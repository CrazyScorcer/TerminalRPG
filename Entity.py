import math,textwrap,random
from enum import Enum

class Entity():
    def __init__(self, _Type: str, _Name:str, _statDic: dict) -> None:
        self.Type = _Type 
        self.Name = _Name
        self.LVL = _statDic['LVL']
        self.HP = _statDic['HP']
        self.MaxHP = _statDic['HP']
        self.ATK = _statDic['ATK']
        self.DEF = _statDic['DEF']
        self.SPD = _statDic['SPD']
        self.isDefending = False
        self.isAlive = True

    def calculateDamage(self,damage):
        damage = damage*math.pow(math.e,(-self.DEF/damage))
        if self.isDefending:
            damage = damage/2

        finalDamage = round(damage) if round(damage) > 1 else 1
        self.HP -= finalDamage

        if self.HP <= 0:
            self.isAlive = False

        return finalDamage

    def printStats(self):
        print(textwrap.dedent(f"""\
        Type = {self.Type}
        Name = {self.Name}
        Health = {self.HP}
        Attack = {self.ATK}
        Defense = {self.DEF}
        Speed = {self.SPD}"""))

class Monster(Entity):
    def __init__(self,_monsterName,_monsterStatsDict) -> None:
        super().__init__("Monster",_monsterName,_monsterStatsDict) 
    
    def randomAction(self):
        return random.choice(["Attack","Defend"])

class Player(Entity):
    class Job(Enum):
        WARRIOR = 1
        MAGE = 2
        THIEF = 3

    jobStatsDictionary = {
        Job.WARRIOR: {
            'MaxHP': 3,
            'ATK': 2,
            'DEF': 3,
            'SPD': 1
        },
        Job.MAGE: {
            'MaxHP': 2,
            'ATK': 4,
            'DEF': 1,
            'SPD': 2    
        },
        Job.THIEF: {
            'MaxHP': 1,
            'ATK': 3,
            'DEF': 2,
            'SPD': 3
        }
    }
    def __init__(self,_playerID,_playerName,_playerStatsDict,_playerJob) -> None:
        super().__init__("Player",_playerName,_playerStatsDict)
        self.playerID = _playerID
        self.playerJob = _playerJob
        self.EXP = 0
        self.MaxEXP = round(math.pow(math.e,self.LVL/100)*(self.LVL+5))
    
    def checkLVL(self):
        if self.EXP < self.MaxEXP:
            return False
        
        self.LVL += 1
        self.EXP -= self.MaxEXP
        self.MaxEXP = round(math.pow(math.e,self.LVL/100)*(self.LVL+5))
        self.eventLVLUP()
        return True
    
    def eventLVLUP(self):
        self.HP += self.jobStatsDictionary[self.playerID]['MaxHP']
        self.MaxHP += self.jobStatsDictionary[self.playerID]['MaxHP']
        self.ATK += self.jobStatsDictionary[self.playerID]['ATK']
        self.DEF += self.jobStatsDictionary[self.playerID]['DEF']
        self.SPD += self.jobStatsDictionary[self.playerID]['SPD']
