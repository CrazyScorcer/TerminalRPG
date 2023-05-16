import Entity
import random
class Monster(Entity.Entity):
    def __init__(self,_monsterName,_monsterLVL,_monsterHP,_monsterATK,_monsterDEF,_monsterSPD) -> None:
        super().__init__("Monster",_monsterName,_monsterLVL,_monsterHP,_monsterATK,_monsterDEF,_monsterSPD) 
    
    def randomAction(self):
        return random.choice(["Attack","Defend"])
    