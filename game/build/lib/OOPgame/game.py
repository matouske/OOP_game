from random import randint, shuffle

class GameInfo():
    """
    The GameInfo class contains methods to create objects in the game, show hepl and others.
    Stores name of author.
    """
    author = "Eva"

    def __init__(self, game_title):
        """
        Creates a GameInfo object which is necessary for the game.

        Args:
            game_title (string): The name of the game.

        Other values:
            secter (dictionary): The real murder room, weapon and killer (you have to reveal them).
            players (int): The number of players in the game including you.
        """
        self.title = game_title
        self._secret = {"room" : None, "item": None, "guest": None}
        self._players = 0

    @property
    def players(self):
        """Gets or sets the number of players in the game."""
        return self._players
    @players.setter
    def players(self, value):
        self._players = value

    def create_rooms(self):
        """
        Creates nine rooms in the game and links them.
        """
        hall = Room("hall")
        hall.description = "A central place of the whole building."
        lounge = Room("lounge")
        lounge.description = "A quiet place for sitting and smoking."
        dining = Room("dining room")
        dining.description = "A large room with ornate golden decorations on each wall."
        kitchen = Room("kitchen")
        kitchen.description = "A dank and dirty room buzzing with flies."
        ballroom = Room("ballroom")
        ballroom.description = "A vast room with a shiny wooden floor; huge candlesticks guard the entrance."
        study = Room("study")
        study.description = "A simply furnished room where zou can write a letter or use computer."
        library = Room("library")
        library.description = "A large collection of books in one place."
        billiard = Room("billiard room")
        billiard.description = "A recreation room with a billiard table."
        sunroom = Room("sunroom")
        sunroom.description = "A place which enable abundant daylight and views of the landscape while sheltering from adverse weather."

        hall.link_room(lounge,"north")
        hall.link_room(study,"south")
        lounge.link_room(hall,"south")
        lounge.link_room(dining,"east")
        lounge.link_room(sunroom, "south-east")
        dining.link_room(lounge,"west")
        dining.link_room(kitchen,"east")
        kitchen.link_room(dining, "west")
        kitchen.link_room(ballroom, "south")
        kitchen.link_room(study, "south-west")
        ballroom.link_room(kitchen,"north")
        ballroom.link_room(sunroom,"south")
        study.link_room(hall,"north")
        study.link_room(library,"east")
        study.link_room(kitchen,"north-east")
        library.link_room(study,"west")
        library.link_room(billiard,"east")
        billiard.link_room(library,"west")
        billiard.link_room(sunroom,"east")
        sunroom.link_room(billiard,"west")
        sunroom.link_room(ballroom,"north")
        sunroom.link_room(lounge,"north-west")

        return hall

    def create_items(self):
        """
        Creates six items (murder weapons).
        """
        index = [0,1,2,3,4,5,6,7,8]
        shuffle(index)
        item_name = ["knife","candlestick","revolver","rope","lead pipe","poison","wrench","scissors","trophy"]
        item_description = ["Often used in a kitchen.",\
        "Some of them are in ballroom.",\
        "Be careful, this weapon has been used before.",\
        "Some of them are in ballroom next to curtains.",\
        "It should be in study.",\
        "It can be mixed in the kitchen.",\
        "Heavy useful thing when you want to turn objects or kill somebody.",\
        "They are often used in sunroom.",\
        "A cup-styled trophy with marble pedestal."]

        for i in index[:6]:
            t = Item(item_name[i])
            t.description = item_description[i]


    def create_chars(self):
        """
        Creates six guests and three policemen.
        """
        index = [0,1,2,3,4,5,6,7,8]
        shuffle(index)
        guest_description = ["yellow","purple","green","blue","red","white","black","pink","orange"]
        guest_name = ["Colonel Mustard", "Professor Plum", "Reverend Green", "Mrs Peacock", "Miss Scarlet", "Mrs White", "General Dark", "Miss Barbie", "Mr Lemonade"]

        for i in index[:6]:
            Guest(guest_name[i], guest_description[i])

        p = ["John", "Peter","George"]
        for i in range(3):
            Police("Policeman "+p[i],"")

    def place_item_chars(self):
        """
        Place items, guests and policemen into a room.
        """
        rooms = Room.rooms
        shuffle(rooms)
        for i in range(6):
            rooms[i].character = Guest.guests[i]
            rooms[8-i].item = Item.items[i]

        for i in range(6,9):
            rooms[i].character = Police.polices[i-6]

    def divide_cards(self):
        """
        Divides cards (Room, Item and Guest):
            1. Selects room, murder weapon and killer.
            2. Shuffle remaining cards.
            3. Splits some cards between Policemen.
            4. Creates Players and splits remaining cards between them.
        """
        cards = []
        cards.extend(Room.rooms)
        cards.extend(Item.items)
        cards.extend(Guest.guests)

        sec = [randint(0,8),randint(9,14),randint(15,20)]
        self._secret["room"] = cards[sec[0]]
        self._secret["item"] = cards[sec[1]]
        self._secret["guest"] = cards[sec[2]]

        del cards[sec[2]]
        del cards[sec[1]]
        del cards[sec[0]]

        division = {3: [2,2,2,6,6],4:[2,1,2,4,5,4],5:[2,1,1,3,4,3,4],6:[1,1,1,3,3,3,3,3]}
        shuffle(cards)
        shuffle(cards)

        index = 0
        for i in range(division[self._players][0]):
            Police.polices[0].add_card(cards[index])
            index += 1
        for i in range(division[self._players][1]):
            Police.polices[1].add_card(cards[index])
            index += 1
        for i in range(division[self._players][2]):
            Police.polices[2].add_card(cards[index])
            index += 1

        for i in range(self._players-1):
            p = Player("Player "+str(i+1),"")
            for j in range(division[self._players][i+3]):
                p.add_card(cards[index])
                index += 1

    def compare(self, room, guest, item):
        """
        Compares your suggestion with information (cards) which have other players.
        Returns a text to be displayed.

        Args:
            room (Room): The suggested room.
            guest (Guest): The suggested guest.
            item (Item): The suggested murder weapon.
        """
        text = "\nYour suggestion: " + room.name + ", " + guest.name + " and " + item.name + "\n"
        for p in Player.players:
            if room in p.get_cards():
                return text + "\t-> "+ p.name + " knows that " + room.name+" isn't place of murder.\n"
            if guest in p.get_cards():
                return text + "\t-> "+ p.name + " knows that " + guest.name+" isn't a killer.\n"
            if item in p.get_cards():
                return text + "\t-> "+ p.name + " knows that " + item.name+" isn't murder weapon.\n"

        return text + "\t-> None of players has an information.\n"

    def accuse(self, room, guest, item):
        """
        Compares your accusion with real murder room, weapon and killer.
        Returns a boolean value indicating success or failure.

        Args:
            room (Room): The room where the murder happened.
            guest (Guest): The guest who is the killer.
            item (Item): The item which is the murder weapon.
        """
        if room == self._secret["room"] and guest == self._secret["guest"] and item == self._secret["item"]:
            print("\nYour accusion: " + room.name + ", " + guest.name + " and " + item.name)
            print("\t is correct.")
            print("Congratulations! YOU WIN!")
            return True
        print("\nYour accusion: " + room.name + ", " + guest.name + " and " + item.name)
        print("\t is not correct.")
        print("The solution was: "+self._secret["room"].name +", "+ self._secret["guest"].name +" and "+ self._secret["item"].name)
        return False

    def welcome(self):
        """
        Prints text which welcomes you to the game.
        """
        print(self.title)
        print("Who did it? Where did it happen? With what weapon?")
        print("Truth is hidden between 6 guests, 9 rooms and 6 weapons.")

    def goal(self):
        """
        Informs you what is a goal of the game.
        """
        print("\nYou and the other " + str(self._players-1) + " players are trying to solve a murder of Mr Bob.")
        print("First, take a walk around the house. Search all 9 rooms, find 6 possible murder weapons (denoted as items) and find out who was present in the house (6 guests).")
        print("Police officers are in some rooms and they can help you. They can tell you what they have already found.")
        print("After exploring the rooms, you can compare your suggestion with other players. However, they won't tell you everything. Your suggestion is compared to information which knows the first player. If he knows about any of your suggestion, he will reveal one piece of information to you. If not, the same comparison is done to the second player's information, etc. You can make a suggestion as to the details, naming a suspect and weapon. Room suggestion depends on the room in which you are standing.")
        print("You can write your findings in the block.")
        print("When you believe that you have determined the correct elements, you can make an accusation. The accusation consists of the room, guest and weapon. You win when your accusation is correct, otherwise you lose. You have only one try.")

    @staticmethod
    def info():
        """
        Prints information about creator.
        """
        print("Made using the OOP RPG Creator (c) me")

    @classmethod
    def credits(cls):
        """
        Prints credits.
        """
        print("\nThank you for playing")
        print("Created by "+cls.author)

    @staticmethod
    def help():
        """
        Returns a text containing a list of commands to be displayed.
        """
        text = '\n'
        text += 'List of commands:\n'
        text += "\tnorth, south, east, west, south-west, south-east, north-west, north-east ... move between rooms\n"
        text += "\texplore ... explore what is in a room\n"
        text += "\tinfo item ...list of items (murder weapons), which you found, containing your notes\n"
        text += "\tinfo guest ...list of guests, which you met, containing your notes\n"
        text += "\tinfo room ...list of rooms in the house containing your notes\n"
        text += "\tblock ... look at your block (notepad)\n"
        text += "\twrite item ... write note to a item into your block\n"
        text += "\twrite guest ... write note to a guest into your block\n"
        text += "\twrite room ... write note to a room into your block\n"
        text += "\ttalk ... speak with somebody in a room\n"
        text += "\t\tend ... end of discussion\n"
        text += "\tcompare ... compare your suggestion with other players\n"
        text += "\taccuse ... make an accusation\n"
        text += "\thelp ... display this list of commands\n"
        text += "\tmap ... display a map\n"
        text += "\texit ... exit game\n"
        return text

    @staticmethod
    def map():
        """
        Returns a text containing a map of linked rooms to be displayed.
        """
        text = '\n'
        text += 'Map:\n'
        text += "lounge-------dining room-------kitchen\n"
        text += "|     \                       / |      \n"
        text += "|      \                     /  |      \n"
        text += "|       --------   ----------   |      \n"
        text += "|               \ /             |      \n"
        text += "hall             /             ballroom\n"
        text += "|               / \             |      \n"
        text += "|      ---------   ----------   |      \n"
        text += "|     /                      \  |      \n"
        text += "|    /                        \ |      \n"
        text += "study--library--billiard room--sunroom\n"
        return text

class Room():
    """
    The Room class represents one room and is initialized by passing a room name.
    Stores all created rooms in a list 'Room.rooms'.
    """
    rooms = []
    def __init__(self, room_name):
        """
        Creates a Room object which connect other classes in the game.

        Args:
            room_name (string): The name of the room.

        Other values:
            description (string): The description of the room.
            full_describe (boolean): The value indicates whether the room was explored.
            linked_rooms (dict): The dictionary containing all adjacent rooms, the key indicates the direction of the door.
            character (Character/Guest/Police): The character standing in the room.
            item (Item): The item which is in the room.
            note (string): The note added to the room.
            command (int): The value assigned to the room.
        """
        self._name = room_name
        self._description = ""
        self._full_describe = False
        self.linked_rooms = {}
        self._character = None
        self._item = None
        self._note = ''
        self._command = 0
        Room.rooms.append(self)


    @property
    def name(self):
        """Gets or sets the name of the room."""
        return self._name
    @name.setter
    def name(self, room_name):
        self._name = room_name

    @property
    def description(self):
        """Gets or sets the description of the room."""
        return self._description
    @description.setter
    def description(self, room_description):
        self._description = room_description

    @property
    def full_describe(self):
        """Gets or sets the value indicating a room exploration."""
        return self._full_describe
    @full_describe.setter
    def full_describe(self, describe):
        self._full_describe = describe

    def link_room(self, room_to_link, direction):
        """
        Add door which links a rooms together.

        Args:
            room_to_link (Room): The Room object.
            direction (string): The direction in which to link the adjacent room.
        """
        self.linked_rooms[direction] = room_to_link
        #print( self.name + " linked rooms :" + repr(self.linked_rooms) )

    @property
    def character(self):
        """Gets or sets the character (Guest/Policeman) in the room."""
        return self._character
    @character.setter
    def character(self, new_character):
        self._character = new_character

    @property
    def item(self):
        """Gets or sets the item in the room."""
        return self._item
    @item.setter
    def item(self, new_item):
        self._item = new_item

    @property
    def note(self):
        """Gets or sets the note to the room."""
        return self._note
    @note.setter
    def note(self, note):
        self._note = note

    @property
    def command(self):
        """Gets or sets the command to the room."""
        return self._command
    @command.setter
    def command(self, command):
        self._command = command

    def get_content(self):
        """
        Finds out if there is an item and/or a character in the room.
        Returns 2 boolean values: item present, character present
        """
        item = False
        if self.item:
            item = True
        if self.character:
            self.character.describe()
            return item, True
        return item, False

    def move(self, direction):
        """
        Move to another room based on the given direction.
        Returns adjacent room (if is in that direction) or current room.

        Args:
            direction (string): The direction in which to move.
        """
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print("\tYou can't go that way.")
            return self

    def describe(self):
        """
        Prints description of the room.
        """
        print(self.name)
        print("--------------------")
        print(self.description)
        if len(self.linked_rooms) > 0:
            self.get_details()
        if self.full_describe:
            self.get_more_details()

    def get_details(self):
        """
        Prints adjacent rooms.
        """
        print("Doors:")
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print("\t[" + direction + "]: " + room.name)

    def get_more_details(self):
        """
        Prints items and characters in the room.
        """
        item = False
        if self.item:
            self.item.describe()
            item = True
        if self.character:
            self.character.describe()
            return item, True
        if not item:
            print("I don't see anything special.")
        return item, False
        
class Item():
    """
    The Item class represents one item and is initialized by passing a item name.
    Stores all created items in a list 'Item.items'.
    """
    items = []

    def __init__(self, item_name):
        """
        Creates a Item object.

        Args:
            item_name (string): The name of the item.

        Other values:
            description (string): The description of the item.
            note (string): The note added to the item.
            command (int): The value assigned to the item.
        """
        self._name = item_name
        self._description = ""
        self._note = ''
        self._command = 0
        Item.items.append(self)

    @property
    def name(self):
        """Gets or sets the name of the item."""
        return self._name
    @name.setter
    def name(self, item_name):
        self._name = item_name

    @property
    def description(self):
        """Gets or sets the description of the item."""
        return self._description
    @description.setter
    def description(self, item_description):
        self._description = item_description

    @property
    def note(self):
        """Gets or sets the note tothe item."""
        return self._note
    @note.setter
    def note(self, note):
        self._note = note

    @property
    def command(self):
        """Gets or sets the command to the item."""
        return self._command
    @command.setter
    def command(self, command):
        self._command = command

    def describe(self):
        """
        Prints the name and description of the item.
        """
        print("The "+self._name + ' is lying here.')
        print("\t"+self.description)


class Character():
    """
    The Character class represents one character and is initialized by passing a character name and description.
    """
    def __init__(self, char_name, char_description):
        """
        Creates a generic 'character' object which contains properties common to all characters.

        Args:
            char_name (string): The name of the character.
            description (string): The description of the character.
        """
        self._name = char_name
        self._description = char_description
        self.conversation = ["I will not speak without my lawyer.","I didn't see anything odd.", "I don't want to talk about it.", "What happened is terrible.", "I'm afraid I can't help you."]

    @property
    def name(self):
        """Gets or sets the name of the character."""
        return self._name
    @property
    def description(self):
        return self._description

    # Describe this character
    def describe(self):
        """
        Prints the name of character and "is here".
        """
        print( self._name + " is here." )

    def talk(self, index):
        """
        Allows to speak with a character.

        Args:
            index (int): The value by which the answer is selected.
        """
        if self.conversation is not None:
            print("\t[" + self._name + " says]: " + self.conversation[index])
        else:
            print("\t" + self._name + " doesn't want to talk to you")


class Guest(Character):
    """
    The Guest subclass of Character represents guest (possible killer).
    Stores all created guests in a list 'Guest.guests'.
    """
    guests = []

    def __init__(self, char_name, char_description):
        """
        Overrides the Character constructor because guest requires note and command variables.

        Args:
            char_name (string): The name of the guest.
            description (string): The description of the guest.

        Other values:
            note (string): The note added to the guest.
            command (int): The value assigned to the guest.
        """
        super().__init__(char_name, char_description)
        self._note = ''
        self._command = 0
        Guest.guests.append(self)

    @property
    def note(self):
        """Gets or sets the note to the guest."""
        return self._note
    @note.setter
    def note(self, note):
        self._note = note

    @property
    def command(self):
        """Gets or sets the command to the guest."""
        return self._command
    @command.setter
    def command(self, command):
        self._command = command


class Player(Character):
    """
    The Player subclass of Character represents players in the game except you.
    Stores all created players in a list 'Player.players'.
    """
    players = []

    def __init__(self, char_name, char_description):
        """
        Overrides the Character constructor because player stores a list of cards (verified information which they can compare with your suggestion).

        Args:
            char_name (string): The name of the player.
            description (string): The description of the player.

        Other values:
            cards (list): The list of Room/Item/Guest objects.
        """
        super().__init__(char_name, char_description)
        self.cards = []
        Player.players.append(self)

    def add_card(self, card):
        """
        Adds object to the list.

        Args:
            card (Room/Guest/Item): The object to be added.
        """
        self.cards.append(card)

    def get_cards(self):
        """
        Returns a list of stored objects.
        """
        return self.cards

class Police(Character):
    """
    The Police subclass of Character represents policeman who can help you.
    Stores all created policemen in a list 'Police.polices'.
    """
    polices = []

    def __init__(self, char_name, char_description):
        """
        Overrides the Character constructor because policeman stores a list of cards (verified information which they provide to you). They also have different talk mthod.

        Args:
            char_name (string): The name of the policeman.
            description (string): The description of the policeman.

        Other values:
            cards (list): The list of Room/Item/Guest objects.
        """
        super().__init__(char_name, char_description)
        self.cards = []
        Police.polices.append(self)

    def add_card(self, card):
        """
        Adds object to the list.

        Args:
            card (Room/Guest/Item): The object to be added.
        """
        self.cards.append(card)

    def get_cards(self):
        """
        Returns a list of stored objects.
        """
        return self.cards

    def talk(self, index):
        """
        Overrides the talk method.

        Args:
            index (int): The value by which the answer is selected.
        """
        text = ''
        text += "\t[Policeman]: I've found this so far:\n"
        for i in self.cards:
            if isinstance(i, Item):
                text += "\t\t"+i.name+" isn't murder weapon\n"
            elif isinstance(i, Room):
                text += "\t\t"+i.name+" isn't place of murder\n"
            else:
                text += "\t\t"+i.name+" isn't a killer\n"
        return text
        

def game_start():
    game = GameInfo("Solve a murder mystery!")
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
        

    def block_content(inventory, name, with_command, form="\t"):
        text = ''
        if with_command:
            for i in inventory[name]:
                text += form + "[{:<1}] {:<16} {:<30}\n".format(str(i.command), i.name, i.note)
        else:
            text += form + "{:<16} {:<30}\n".format("", "note")
            for i in inventory[name]:
                text += form + "{:<16} {:<30}\n".format(i.name, i.note)
        return text



    inventory = {"items": [], "guests": [], "rooms": []}
    text = ''
    item = False
    character = False
    directions = ["north", "south", "east", "west", "south-west", "south-east", "north-west", "north-east"]
    exploring = True
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
                text += block_content(inventory, "items", False)
            else:
                text += "\tnothing\n"

        elif command == "info guest": # which guests are here
            text += "\nFound guests:\n"
            if inventory["guests"]:
                text += block_content(inventory, "guests", False)
            else:
                text += "\tnobody\n"

        elif command == "info room": # which guests are here
            text += "\nVisited rooms:\n"
            text += block_content(inventory, "rooms", False)

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
                text += block_content(inventory, "rooms", False, "\t\t")
                w += 1
            if inventory["guests"]:
                text += "\tGuests:\n"
                text += block_content(inventory, "guests", False, "\t\t")
                w += 1
            if inventory["items"]:
                text += "\tItems:\n"
                text += block_content(inventory, "items", False, "\t\t")
                w += 1
            if w == 0:
                text += "\tnothing\n"

        elif command == "write room":
            if exploring:
                text += "You need to explore more.\n"
            else:
                print("\tYour notes:")
                print(block_content(inventory, "rooms", True, "\t\t"))
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
                print(block_content(inventory, "guests", True, "\t\t"))
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
                print(block_content(inventory, "items", True, "\t\t"))
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
                print(block_content(inventory, "guests", True, "\t\t"))
                guest = True
                while guest:
                    g = int(input("\tSelect guest (write a number from the table): "))
                    if g > len(inventory["guests"]):
                        print("\t\t" + str(g) + " is not valid.")
                    else:
                        guest = False
                print("\n\tItems:")
                print(block_content(inventory, "items", True, "\t\t"))
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
                print(block_content(inventory, "rooms", True, "\t\t"))
                room = True
                while room:
                    r = int(input("\tSelect room (write a number from the table): "))
                    if r > len(inventory["rooms"]):
                        print("\t\t" + str(r) + " is not valid.")
                    else:
                        room = False
                print("\n\tGuests:")
                print(block_content(inventory, "guests", True, "\t\t"))
                guest = True
                while guest:
                    g = int(input("\tSelect guest (write a number from the table): "))
                    if g > len(inventory["guests"]):
                        print("\t\t" + str(g) + " is not valid.")
                    else:
                        guest = False
                print("\n\tItems:")
                print(block_content(inventory, "items", True, "\t\t"))
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
