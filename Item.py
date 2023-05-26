class Item:
    def __init__(self, _itemID: int, s) -> None:
        self.itemID = _itemID

class Armor(Item):
    def __init__(self, _itemID: int) -> None:
        super.__init__(_itemID)
        pass

class Weapon(Item):
    def __init__(self, _itemID: int) -> None:
        super.__init__(_itemID)
        pass
