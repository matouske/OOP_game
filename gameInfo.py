from room import Room
from item import Item
from character import Guest, Player, Police
from random import randint, shuffle

class GameInfo():
    """
    The GameInfo class contains methods to create objects in the game, show hepl and others.
    Stores name of author.
    """
    author = "Anonymous"

    def __init__(self, game_title, author):
        """
        Creates a GameInfo object which is necessary for the game.

        Args:
            game_title (string): The name of the game.
            author (string): The name of the author of this game.

        Other values:
            secter (dictionary): The real murder room, weapon and killer (you have to reveal them).
            players (int): The number of players in the game including you.
        """
        self.title = game_title
        self.author = author
        self._secret = {"room" : None, "item": None, "guest": None}
        self._players = 0

    @property
    def players(self):
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
