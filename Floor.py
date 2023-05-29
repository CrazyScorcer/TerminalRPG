from Entity import Monster
import random,sqlite3

class Floor:
    def __init__(self,_roomAmount: int, _playerLVL: int) -> None:
        self.roomAmount = _roomAmount
        self.playerLVL = _playerLVL
        self.roomList = []
        self.generateFloor()

    def generateFloor(self) -> None:
        connection = sqlite3.connect('Info.db')
        cursor = connection.cursor()
        for i in range(self.roomAmount):
            monsterRoomId = random.randint(1,3)
            monsterRoomInfo = cursor.execute('Select MonsterAmount, Difficulty From MonsterRoomInfo Where MonsterRoomID = ?',(monsterRoomId,)).fetchone()
            self.roomList.append(MonsterRoom(monsterRoomId,monsterRoomInfo,self.playerLVL))
            monsterRoomInfo = cursor.execute('Select MonsterAmount, Difficulty From MonsterRoomInfo Where MonsterRoomID = 4').fetchone()
        self.roomList.append(MonsterRoom(4,monsterRoomInfo,self.playerLVL))

class MonsterRoom:
    def __init__(self,_monsterRoomType: int,_monsterRoomInfo: tuple,_baseStat: int) -> None:
        self.monsterRoomType = _monsterRoomType
        self.monsterRoomInfo = _monsterRoomInfo
        self.baseStat = _baseStat
        self.monsterList = [] if self.monsterRoomType > 4 else self.monsterGenerate()
    
    def monsterGenerate(self) -> list:
        monsterList = []
        for index in range(self.monsterRoomInfo[0]):
            monsterStatsDict = {
                'LVL': 1,
                'MaxHP': random.randint(self.baseStat-3+self.monsterRoomInfo[1], self.baseStat+1+self.monsterRoomInfo[1]),
                'ATK': random.randint(self.baseStat-3+self.monsterRoomInfo[1], self.baseStat+1+self.monsterRoomInfo[1]),
                'DEF': random.randint(self.baseStat-3+self.monsterRoomInfo[1], self.baseStat+1+self.monsterRoomInfo[1]),
                'SPD': random.randint(self.baseStat-3+self.monsterRoomInfo[1], self.baseStat+1+self.monsterRoomInfo[1])
            }
            # Prevent any stats from being 0 or less
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