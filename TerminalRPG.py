import Floor
from Entity import Player
import textwrap, random, sqlite3, sys, time

def printPlayerBattleActions():
    print(textwrap.dedent("""\
    A: Attack
    D: Defend
    R: Run Away"""))

def printStartOptions():
    print(textwrap.dedent("""\
    N: New Character
    S: Open Save
    Q: Quit Game"""))

def printSavedCharacters():
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

def printCurrentBattleHP(entityList: list):
    print(textwrap.dedent(f"""\
    Player:
    {entityList[0].Name} LVL:{entityList[0].LVL} HP:{entityList[0].HP}/{entityList[0].MaxHP} EXP:{entityList[0].EXP}/{entityList[0].MaxHP}
    Enemies:"""))
    for entity in entityList[1:]:
        print(f"{entity.Name} LVL:{entity.LVL} HP:{entity.HP}/{entity.MaxHP}", end=" ")
    print("")

def defineActionOrder(entityList: list):
    actionOrder = []
    for index,entity in enumerate(entityList):
        if len(actionOrder) == 0:
            actionOrder.append(index)
        else:
            inActionOrder = False
            for i in range(len(actionOrder)):
                if entityList[actionOrder[i]].SPD < entity.SPD:
                    actionOrder.insert(i,index)
                    inActionOrder = True
                    break
            if not inActionOrder:
                actionOrder.append(index)
    return actionOrder

def initBattle(entityList: list):
    print("Monsters Encounter")
    actionOrder = defineActionOrder(entityList)
    currentTurn = 0
    while True:
        time.sleep(.25)
        # If the player is the only one alive, End Battle
        if len(entityList) == 1:
            print("Battle Won!")
            break
        # Current Turn is Player
        if entityList[actionOrder[currentTurn]].Type == "Player":
            entityList[0].isDefending = False
            printCurrentBattleHP(entityList)
            printPlayerBattleActions()
            userInput = input("Choose your action: ").upper()
            print("-------------------------------------------------------------------------")
            if userInput == 'A':
                selectedMonster = 1
                if len(entityList) > 2:
                    while True:
                        try:
                            selectedMonster = int(input(f"Select Enemy to Attack(1-{len(entityList)-1}): "))
                            print("-------------------------------------------------------------------------")
                            break
                        except ValueError:
                            print("Invalid Input. Input an Integer.")

                print(f"{entityList[0].Name} attacked {entityList[selectedMonster].Name} for {entityList[selectedMonster].calculateDamage(entityList[0].ATK)}")
                print("-------------------------------------------------------------------------")
                time.sleep(.25)
                if not entityList[selectedMonster].isAlive:
                    print(f"{entityList[0].Name} defeated {entityList[selectedMonster].Name}")
                    print("-------------------------------------------------------------------------")
                    entityList[0].EXP += entityList[selectedMonster].LVL
                    time.sleep(.25)
                    if entityList[0].checkLVL():
                        print(f"{entityList[0].Name} Leveled UP!\nYou are now Level {entityList[0].LVL}")
                        print("-------------------------------------------------------------------------")
                    entityList.pop(selectedMonster)
                    actionOrder = defineActionOrder(entityList)

            elif userInput == 'D':
                entityList[0].isDefending = True
            # End battle
            elif userInput == 'R':
                print("You Ran Away Successfully")
                # Add Weighted Run Away
                break
            else:
                print("Invalid Input. Input a Valid Action")
                printPlayerBattleActions()
        # Current Turn is Enemy
        else:
            entityList[actionOrder[currentTurn]].isDefending = False
            monsterAction = entityList[actionOrder[currentTurn]].randomAction()
            if monsterAction == "Attack":
                print(f"{entityList[actionOrder[currentTurn]].Name} attacked {entityList[0].Name} for {entityList[0].calculateDamage(entityList[actionOrder[currentTurn]].ATK)}")
            else:
                entityList[actionOrder[currentTurn]].isDefending = True
                print(f"{entityList[actionOrder[currentTurn]].Name} is Defending")
            print("-------------------------------------------------------------------------")

        # If the player dies during the fight, End Battle
        if not entityList[0].isAlive :
            break
        
        currentTurn += 1
        currentTurn %= len(entityList)

    return entityList[0]

def createNewPlayer():
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    
    while True:
        print(textwrap.dedent("""\
            1.Warrior: High HP, High DEF, Moderate ATK, Low SPD
            2.Mage: Ultra ATK, Moderate HP, Moderate SPD, LOW DEF
            3.Thief: High ATK, High SPD, Moderate DEF, Low HP"""))
        
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
            playerID = cursor.execute("SELECT COUNT(*) FROM PlayerInfo").fetchone()[0]+1 # Gets the next valid id / Implementation is faulty, will need to change
            playerStatsDict = {
                'LVL': 1,
                'HP': Player.jobStatsDictionary[job]['MaxHP'],
                'ATK': Player.jobStatsDictionary[job]['ATK'],
                'DEF': Player.jobStatsDictionary[job]['DEF'],
                'SPD': Player.jobStatsDictionary[job]['SPD']
            }
            seed = random.randint(1,100_000_000_000)
            random.seed(seed)
            cursor.execute("INSERT INTO PlayerInfo VALUES (?,?,?,?,?,?,?,?,?,?,?)",(playerID,name,playerStatsDict["HP"],playerStatsDict["HP"],playerStatsDict["ATK"],playerStatsDict["DEF"],playerStatsDict["SPD"],0,playerStatsDict["LVL"],seed,int(job)))
            cursor.commit()
            return Player(name,playerStatsDict,job)
        except Exception as e:
            print(e)
            continue
        finally:
            connection.close()

def createSavedPlayer(characterList):
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    userInput = input("Input Saved Character Name or Back to return to main menu: ")

    if userInput == "Back":
            return None
    
    # Continiously ask for valid character name
    while True:
        if userInput in characterList:        
            try:
                playerInfo = cursor.execute("SELECT * FROM PlayerInfo WHERE PlayerName=?",(userInput,)).fetchone()
                playerStatsDict = {
                'LVL': 1,
                'HP': playerInfo[3],
                'ATK': playerInfo[4],
                'DEF': playerInfo[5],
                'SPD': playerInfo[6]
                }
                player = Player(userInput,playerInfo[1],playerStatsDict,playerInfo[10])
                player.EXP = playerInfo[7]
                player.HP = playerInfo[2]
                random.seed(playerInfo[9])
                return player
            except Exception as e:
                print(e)
                continue
            finally:
                connection.close()
        
        else:
            userInput = input("Invalid character name. Input an existing character name: ")

def savePlayer(player: Player):
    connection = sqlite3.connect("Info.db")
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE PlayerInfo SET HP=?, MaxHP=?, ATK=?, DEF=?, SPD=?, EXP=?, LVL=? WHERE PlayerName=?",(player.HP,player.MaxHP,player.ATK,player.DEF,player.SPD,player.EXP,player.LVL,player.Name))
        connection.commit()
        # return True
    except Exception as e:
        print(e)
        # return False
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
    for room in floor.roomList:
        entityList = room.monsterList
        entityList.insert(0,player)
        player = initBattle(entityList)

        if not player.isAlive:
            print("Game Over")
            break
    
    # savePlayer(player)