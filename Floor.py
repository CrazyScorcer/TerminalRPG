import Monster
from enum import Enum
import random

class RoomType(Enum):
    MONSTER1 = 1
    MONSTER2 = 2
    MONSTER3 = 3
    BOSS = 4

roomStatsDictionary = {
    RoomType.MONSTER1: {
        'MonsterAmount': 1,
        'Difficulty': 3
    },
    RoomType.MONSTER2: {
        'MonsterAmount': 2,
        'Difficulty': 2
    },
    RoomType.MONSTER3: {
        'MonsterAmount': 3,
        'Difficulty': 1
    },
    RoomType.BOSS: {
        'MonsterAmount': 1,
        'Difficulty': 6
    }
}

class Floor:
    def __init__(self,_roomAmount, _seed, _playerLVL) -> None:
        self.roomAmount = _roomAmount
        self.seed = _seed
        self.playerLVL = _playerLVL
        self.roomList = []
        self.generateFloor()

    def generateFloor(self):
        random.seed(self.seed)
        for i in range(self.roomAmount):
            self.roomList.append(Room(RoomType(random.randint(1,3)),self.playerLVL))
        self.roomList.append(Room(RoomType.BOSS,self.playerLVL))

class Room:
    def __init__(self,_roomType: RoomType,_baseStat) -> None:
        self.roomType = _roomType
        self.baseStat = _baseStat
        self.roomStats = roomStatsDictionary[self.roomType]
        self.monsterList = [] if _roomType.value > 4 else self.monsterGenerate(self.roomStats['MonsterAmount'],self.roomStats['Difficulty'])
    
    def monsterGenerate(self,monsterAmount,difficulty):
        monsterList = []
        for index in range(monsterAmount):
            monsterStats = []
            for jdex in range(5):
                monsterStats.append(random.randint(self.baseStat-3+difficulty, self.baseStat+1+difficulty))
                if monsterStats[jdex] < 1:
                    monsterStats[jdex] = 1
            monsterList.append(Monster.Monster(f"Monster{index+1}", monsterStats[0],  monsterStats[1],  monsterStats[2],  monsterStats[3],  monsterStats[4]))
        return monsterList