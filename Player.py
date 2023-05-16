import Entity
import math
from enum import Enum

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

class Player(Entity.Entity):
    def __init__(self,_playerID,_playerName,_playerLVL,_playerHP,_playerATK,_playerDEF,_playerSPD,_seed,_playerJob) -> None:
        super().__init__("Player",_playerName,_playerLVL,_playerHP,_playerATK,_playerDEF,_playerSPD)
        self.playerID = _playerID
        self.jobStatUp = jobStatsDictionary[_playerJob]
        self.EXP = 0
        self.MaxEXP = round(math.pow(math.e,self.LVL/100)*(self.LVL+5))
        self.seed = _seed
    
    def checkLVL(self):
        if self.EXP < self.MaxEXP:
            return False
        
        self.LVL += 1
        self.EXP -= self.MaxEXP
        self.MaxEXP = round(math.pow(math.e,self.LVL/100)*(self.LVL+5))
        self.eventLVLUP()
        return True
    
    def eventLVLUP(self):
        self.HP += self.jobStatUp['MaxHP']
        self.MaxHP += self.jobStatUp['MaxHP']
        self.ATK += self.jobStatUp['ATK']
        self.DEF += self.jobStatUp['DEF']
        self.SPD += self.jobStatUp['SPD']
