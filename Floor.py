from Entity import Monster
from enum import Enum
import random

class MonsterRoomType(Enum):
    MONSTER1 = 1
    MONSTER2 = 2
    MONSTER3 = 3
    BOSS = 4

MonsterRoomStatsDictionary = {
    MonsterRoomType.MONSTER1: {
        'MonsterAmount': 1,
        'Difficulty': 3
    },
    MonsterRoomType.MONSTER2: {
        'MonsterAmount': 2,
        'Difficulty': 2
    },
    MonsterRoomType.MONSTER3: {
        'MonsterAmount': 3,
        'Difficulty': 1
    },
    MonsterRoomType.BOSS: {
        'MonsterAmount': 1,
        'Difficulty': 6
    }
}

class Floor:
    def __init__(self,_roomAmount: int, _playerLVL: int) -> None:
        self.roomAmount = _roomAmount
        self.playerLVL = _playerLVL
        self.roomList = []
        self.generateFloor()

    def generateFloor(self):
        for i in range(self.roomAmount):
            self.roomList.append(MonsterRoom(MonsterRoomType(random.randint(1,3)),self.playerLVL))
        self.roomList.append(MonsterRoom(MonsterRoomType.BOSS,self.playerLVL))

class MonsterRoom:
    def __init__(self,_MonsterRoomType: MonsterRoomType,_baseStat: int) -> None:
        self.MonsterRoomType = _MonsterRoomType
        self.baseStat = _baseStat
        self.roomStats = MonsterRoomStatsDictionary[self.MonsterRoomType]
        self.monsterList = [] if _MonsterRoomType.value > 4 else self.monsterGenerate(self.roomStats['MonsterAmount'],self.roomStats['Difficulty'])
    
    def monsterGenerate(self,monsterAmount: int, difficulty: int):
        monsterList = []
        for index in range(monsterAmount):
            monsterStatsDict = {
                'LVL': 1,
                'HP': 0,
                'ATK': 0,
                'DEF': 0,
                'SPD': 0
            }
            for key in monsterStatsDict:
                if monsterStatsDict[key] < 1:
                    monsterStatsDict[key] = 1
            monsterList.append(Monster(f"Monster{index+1}", monsterStatsDict))
        return monsterList
    
class EventRoom:
    def __init__(self) -> None:
        pass

class TreasureRoom:
    def __init__(self, ) -> None:

        pass