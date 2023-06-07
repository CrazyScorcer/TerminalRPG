import Floor
from Entity import Player,Entity,Monster
from Equipment import Armor, Weapon
import textwrap, random, sqlite3, sys, time

def printPlayerBattleActions() -> None:
    print(textwrap.dedent("""\
    A: Attack
    D: Defend
    R: Run Away"""))

def printStartOptions() -> None:
    print(textwrap.dedent("""\
    N: New Character
    S: Open Save
    Q: Quit Game"""))

def printSavedCharacters() -> list:
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    resultTuple = cursor.execute("SELECT PlayerName, LVL FROM PlayerInfo").fetchall()
    connection.close()
    if len(resultTuple) == 0:
        return []

    characterList = []
    for result in resultTuple:
        print(f"{result[0]} LVL {result[1]}")
        characterList.append(result[0])
    print("Back")
    return characterList

def printCurrentBattleHP(entityList: list[Entity]) -> None:
    player: Player = entityList[0]
    print(textwrap.dedent(f"""\
    Player:
    {player.Name} LVL:{player.LVL} HP:{player.finalStats['HP']}/{player.finalStats['MaxHP']} EXP:{player.EXP}/{player.MaxEXP}
    Enemies:"""))
    for entity in entityList[1:]:
        print(f"{entity.Name} LVL:{entity.LVL} HP:{entity.HP}/{entity.MaxHP}", end=" ")
    print("")

def defineActionOrder(entityList: list[Entity]) -> list[int]:
    actionOrder: list[int] = []
    for index,entity in enumerate(entityList):
        if len(actionOrder) == 0:
            actionOrder.append(index)
        else:
            inActionOrder = False
            for i in range(len(actionOrder)):
                if actionOrder[i] == 0: # entity 0 is the player
                    player: Player = entityList[0]
                    speedCheck = player.finalStats["SPD"]
                else:
                    speedCheck = entityList[actionOrder[i]].SPD
                    
                if speedCheck < entity.SPD:
                    actionOrder.insert(i,index)
                    inActionOrder = True
                    break
            if not inActionOrder:
                actionOrder.append(index)
    return actionOrder

def initBattle(entityList: list[Entity]) -> Player:
    print("Monsters Encountered")
    actionOrder = defineActionOrder(entityList)
    currentTurn = 0
    player: Player = entityList[0]
    while True:
        time.sleep(.25)
        # If the player is the only one alive, End Battle
        if len(entityList) == 1:
            print("Battle Won!")
            break
        # Current Turn is Player
        if actionOrder[currentTurn] == 0:
            player.isDefending = False
            printCurrentBattleHP(entityList)
            printPlayerBattleActions()
            userInput = input("Choose your action: ").upper()
            print("-------------------------------------------------------------------------")
            if userInput == 'A':
                monsterChoice = 1
                if len(entityList) > 2:
                    while True:
                        try:
                            monsterChoice = int(input(f"Select Enemy to Attack(1-{len(entityList)-1}): "))
                            print("-------------------------------------------------------------------------")
                            break
                        except ValueError:
                            print("Invalid Input. Input an Integer.")
                        except IndexError:
                            print(f"Invalud Input. Select Value in range(1-{len(entityList)-1}):")
                selectedMonster: Monster = entityList[monsterChoice]
                print(f"{player.Name} attacked {selectedMonster.Name} for {selectedMonster.calculateDamage(player.finalStats['ATK'])}")
                print("-------------------------------------------------------------------------")
                time.sleep(.25)
                if not selectedMonster.isAlive:
                    print(f"{player.Name} defeated {selectedMonster.Name}")
                    print("-------------------------------------------------------------------------")
                    player.EXP += selectedMonster.LVL
                    time.sleep(.25)
                    if player.checkLVL():
                        print(f"{player.Name} Leveled UP!\nYou are now Level {player.LVL}")
                        print("-------------------------------------------------------------------------")
                    entityList.pop(monsterChoice)
                    actionOrder = defineActionOrder(entityList)

            elif userInput == 'D':
                player.isDefending = True
            # End battle
            elif userInput == 'R':
                print("You Ran Away Successfully")
                # TODO Add Weighted Run Away
                break
            else:
                print("Invalid Input. Input a Valid Action")
                printPlayerBattleActions()
        # Current Turn is Enemy
        else:
            currentMonster: Monster = entityList[actionOrder[currentTurn]]
            currentMonster.isDefending = False
            
            monsterAction = currentMonster.randomAction()
            if monsterAction == "Attack":
                print(f"{currentMonster.Name} attacked {player.Name} for {player.calculateDamage(currentMonster.ATK)}")
            else:
                currentMonster.isDefending = True
                print(f"{currentMonster.Name} is Defending")
            print("-------------------------------------------------------------------------")

        # If the player dies during the fight, End Battle
        if not entityList[0].isAlive :
            break
        
        currentTurn += 1
        currentTurn %= len(entityList)

    return entityList[0]

def createNewPlayer() -> Player:
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    
    while True:
        print(textwrap.dedent("""\
            1.Warrior: High HP, High DEF, Moderate ATK, Low SPD
            2.Mage: Ultra ATK, Moderate HP, Moderate SPD, LOW DEF
            3.Thief: High ATK, High SPD, Moderate DEF, Low HP"""))
        # Request User for valid JobID
        job = input("Choose a number corresponding to a class or Back to return to main menu: ")
        while True:
            if job == "Back":
                return None         
            try:
                if int(job) > 0 and int(job) <= 3 :
                    break
            except ValueError:
                print("Invalid input.", end="") 
            job = input("Please input a valid class number or Back: ")
        jobStats = cursor.execute("SELECT MaxHP, ATK, DEF, SPD FROM Jobs WHERE JobID = ?",(job)).fetchone()

        # Request User for valid Name
        name = input("Input the name of your Character or Back to return to main menu: ")
        while True:
            if name == "Back":
                return None
            # Check if PlayerName Exists
            elif (cursor.execute("SELECT Count(*) FROM PlayerInfo WHERE PlayerName=?",(name,)).fetchone()[0] != 0):
                name = input("Name already exists. Try again.")
            else:
                break

        try:    
            playerStatsDict = {
                'LVL': 1,
                'HP': jobStats[0],
                'ATK': jobStats[1],
                'DEF': jobStats[2],
                'SPD': jobStats[3]
            }
            seed = random.randint(1,100_000_000_000)
            # random.seed(seed)
            cursor.execute("INSERT INTO PlayerInfo VALUES (?,?,?,?,?,?,?,?,?,?)",(name,playerStatsDict["HP"],playerStatsDict["HP"],playerStatsDict["ATK"],playerStatsDict["DEF"],playerStatsDict["SPD"],0,playerStatsDict["LVL"],seed,int(job)))
            connection.commit()
            connection.close()
            return Player(name,playerStatsDict,job,jobStats)
        except Exception as e:
            print(e)
            exit()

def createSavedPlayer(characterList) -> None:
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    userInput = input("Input Saved Character Name or Back to return to main menu: ")

    if userInput == "Back":
        return None
    
    # Continiously ask for valid character name and construct player if valid name
    while True:
        if userInput in characterList:        
            playerInfo = cursor.execute("SELECT LVL,HP,MaxHP,ATK,DEF,SPD,EXP,Seed,JobID FROM PlayerInfo WHERE PlayerName=?",(userInput,)).fetchone()
            jobStats = cursor.execute("SELECT MaxHP, ATK, DEF, SPD FROM Jobs WHERE JobID = ?",(playerInfo[8],)).fetchone()
            playerArmorTuples = cursor.execute("SELECT Armor.Name, ArmorType.Name, Armor.HP, Armor.DEF, Armor.SPD FROM ((PlayerArmor Inner Join Armor ON PlayerArmor.ArmorID = Armor.ArmorID) Inner Join ArmorType ON Armor.ArmorTypeID = ArmorType.ArmorTypeID) WHERE PlayerName = ?",(userInput,)).fetchall()
            playerStatsDict = {
                'LVL': playerInfo[0],
                'MaxHP': playerInfo[2],
                'ATK': playerInfo[3],
                'DEF': playerInfo[4],
                'SPD': playerInfo[5]
            }
            player = Player(userInput,playerStatsDict,playerInfo[8],jobStats)
            player.EXP = playerInfo[6]
            player.HP = playerInfo[1]
            for playerArmorTuple in playerArmorTuples:
                player.equipItem(Armor(playerArmorTuple[1],playerArmorTuple[2],playerArmorTuple[3],playerArmorTuple[4],playerArmorTuple[0]))
            player.updateFinalStats()
            # random.seed(playerInfo[7])
            connection.close()
            return player
                
        else:
            userInput = input("Invalid character name. Input an existing character name: ")

def savePlayer(player: Player):
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE PlayerInfo SET HP=?, MaxHP=?, ATK=?, DEF=?, SPD=?, EXP=?, LVL=? WHERE PlayerName=?",(player.HP,player.MaxHP,player.ATK,player.DEF,player.SPD,player.EXP,player.LVL,player.Name))
        for key in player.equipment:
            if player.equipment[key] is not None:
                # player.equipment[key].updateDB()
                pass
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()

if __name__ == "__main__":
    player = None

    while player is None:
        printStartOptions()
        userInput = input("Select An Option: ").upper()
        if userInput == 'N':
            player = createNewPlayer()    
        elif userInput == 'S':
            characterList = printSavedCharacters()
            if len(characterList) == 0:
                print("No characters exist at this momement")
                continue
            player = createSavedPlayer(characterList)
        elif userInput == 'Q':
            sys.exit("Exit Game")
        else:
            print("Invalid Input")

    floor = Floor.Floor(3,player.LVL)
    room: Floor.MonsterRoom
    for room in floor.roomList:
        entityList = room.monsterList
        entityList.insert(0,player)
        player = initBattle(entityList)

        if not player.isAlive:
            print("Game Over")
            break
    
    # savePlayer(player)