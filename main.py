from character import Guest, Police
from gameInfo import GameInfo
from random import randint

game = GameInfo("Solve a murder mystery!", "Eva")
game.welcome()

run = False
players = 0
command = input("\nDo you want to start? [yes/no] ").lower()
if command == "yes":
    while players == 0:
        players = int(input("Select number of players? [3, 4, 5 or 6] "))
        if players in [3, 4, 5, 6]:
            game.players = players
            print("\tPlayers in the game: player 1-"+str(players-1)+" (computer) and you")
            run = True
        else:
            print("\tWrong answer")

if run:
    # set up rooms
    current_room = game.create_rooms()

    # set up items
    game.create_items()

    # add characters - guests and policemen
    game.create_chars()

    # place people and items
    game.place_item_chars()

    # divide information
    game.divide_cards()

    game.goal()
    print("\n",game.help())

    enter = input("Enter house? [yes/no] ")
    if enter == "yes":
        run = True
    else:
        run = False


inventory = {"items": [], "guests": [], "rooms": []}
text = ''
item = False
character = False
directions = ["north", "south", "east", "west", "south-west", "south-east", "north-west", "north-east"]
exploring = True

def block_content(name, with_command, form="\t"):
    text = ''
    if with_command:
        for i in inventory[name]:
            text += form + "[{:<1}] {:<16} {:<30}\n".format(str(i.command), i.name, i.note)
    else:
        text += form + "{:<16} {:<30}\n".format("", "note")
        for i in inventory[name]:
            text += form + "{:<16} {:<30}\n".format(i.name, i.note)
    return text

while run:
    print("\n")
    current_room.describe()
    print(text, end='')
    text = ''
    command = input("> ").lower()

    if len(inventory["items"]) == 6 and len(inventory["guests"]) == 6 and len(inventory["rooms"]) == 9:
        exploring = False

    if command in directions: # move to a linked room
        current_room = current_room.move(command)
        item = False
        character = False

    elif command == "explore": # what is in the current room
        current_room.full_describe = True
        item, character = current_room.get_content()
        if character:
            if current_room.character not in inventory["guests"] and isinstance(current_room.character, Guest):
                current_room.character.command = len(inventory["guests"])
                inventory["guests"].append(current_room.character)
        if item:
            if current_room.item not in inventory["items"]:
                current_room.item.command = len(inventory["items"])
                inventory["items"].append(current_room.item)
        if current_room not in inventory["rooms"]:
            current_room.command = len(inventory["rooms"])
            inventory["rooms"].append(current_room)

    elif command == "info item": # which items were found
        text += "\nFound items:\n"
        if inventory["items"]:
            text += block_content("items", False)
        else:
            text += "\tnothing\n"

    elif command == "info guest": # which guests are here
        text += "\nFound guests:\n"
        if inventory["guests"]:
            text += block_content("guests", False)
        else:
            text += "\tnobody\n"

    elif command == "info room": # which guests are here
        text += "\nVisited rooms:\n"
        text += block_content("rooms", False)

    elif command == "talk":
        if current_room.full_describe and current_room.character:
            talking = True
            if isinstance(current_room.character,Police):
                text += current_room.character.talk(randint(0,4))
            else:
                while talking:
                    c = input("\t[You say]: ").lower()
                    if c == "bye":
                        talking = False
                        continue
                    current_room.character.talk(randint(0,4))
        else:
            print("\tI don't see anybody to talk to.")

    elif command == "block":
        text += "\nNotes in your block:\n"
        w = 0
        if inventory["rooms"]:
            text += "\tRooms:\n"
            text += block_content("rooms", False, "\t\t")
            w += 1
        if inventory["guests"]:
            text += "\tGuests:\n"
            text += block_content("guests", False, "\t\t")
            w += 1
        if inventory["items"]:
            text += "\tItems:\n"
            text += block_content("items", False, "\t\t")
            w += 1
        if w == 0:
            text += "\tnothing\n"

    elif command == "write room":
        if exploring:
            text += "You need to explore more.\n"
        else:
            print("\tYour notes:")
            print(block_content("rooms", True, "\t\t"))
            thing = True
            while thing:
                t = int(input("\tWrite a number (from the table): "))
                if t > len(inventory["rooms"]):
                    print("\t\t" + str(t) + " is not valid.")
                else:
                    thing = False
            inventory["rooms"][t].note = input("\tYour note: ").lower()

    elif command == "write guest":
        if exploring:
            text += "You need to explore more.\n"
        else:
            print("\tYour notes:")
            print(block_content("guests", True, "\t\t"))
            thing = True
            while thing:
                t = int(input("\tWrite a number (from the table): "))
                if t > len(inventory["guests"]):
                    print("\t\t" + str(t) + " is not valid.")
                else:
                    thing = False
            inventory["guests"][t].note = input("\tYour note: ").lower()

    elif command == "write item":
        if exploring:
            text += "You need to explore more.\n"
        else:
            print("\tYour notes:")
            print(block_content("items", True, "\t\t"))
            thing = True
            while thing:
                t = int(input("\tWrite a number (from the table): "))
                if t > len(inventory["items"]):
                    print("\t\t" + str(t) + " is not valid.")
                else:
                    thing = False
            inventory["items"][t].note = input("\tYour note: ").lower()

    elif command == "compare":
        if exploring:
            text += "You need to explore more before you can compare your thoughts.\n"
        else:
            print("\tGuests:")
            print(block_content("guests", True, "\t\t"))
            guest = True
            while guest:
                g = int(input("\tSelect guest (write a number from the table): "))
                if g > len(inventory["guests"]):
                    print("\t\t" + str(g) + " is not valid.")
                else:
                    guest = False
            print("\n\tItems:")
            print(block_content("items", True, "\t\t"))
            thing = True
            while thing:
                t = int(input("\tSelect item (write a number from the table): "))
                if t > len(inventory["items"]):
                    print("\t\t" + str(t) + " is not valid.")
                else:
                    thing = False
            text += game.compare(current_room, inventory["guests"][g],inventory["items"][t])

    elif command == "accuse":
        if exploring:
            text += "You need to explore more before you can make an accusion.\n"
        else:
            print("\tRooms:")
            print(block_content("rooms", True, "\t\t"))
            room = True
            while room:
                r = int(input("\tSelect room (write a number from the table): "))
                if r > len(inventory["rooms"]):
                    print("\t\t" + str(r) + " is not valid.")
                else:
                    room = False
            print("\n\tGuests:")
            print(block_content("guests", True, "\t\t"))
            guest = True
            while guest:
                g = int(input("\tSelect guest (write a number from the table): "))
                if g > len(inventory["guests"]):
                    print("\t\t" + str(g) + " is not valid.")
                else:
                    guest = False
            print("\n\tItems:")
            print(block_content("items", True, "\t\t"))
            thing = True
            while thing:
                t = int(input("\tSelect item (write a number from the table): "))
                if t > len(inventory["items"]):
                    print("\t\t" + str(t) + " is not valid.")
                else:
                    thing = False
            game.accuse(inventory["rooms"][r], inventory["guests"][g], inventory["items"][t])
            run = False

    elif command == "help":
        text += GameInfo.help()
        continue

    elif command == "map":
        text += GameInfo.map()
        continue

    elif command == "exit":
        run = False
        continue

    else:
        print("\tAction is not possible.")
        continue

game.credits()
