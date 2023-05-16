import math,textwrap
class Entity():
    def __init__(self,_Type,_Name,_LVL,_HP,_ATK,_DEF,_SPD) -> None:
        self.Type = _Type
        self.Name = _Name
        self.LVL = _LVL
        self.HP = _HP
        self.MaxHP = _HP
        self.ATK = _ATK
        self.DEF = _DEF
        self.SPD = _SPD
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
