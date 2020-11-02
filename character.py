from item import Item
from room import Room

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
        return self._note
    @note.setter
    def note(self, note):
        self._note = note

    @property
    def command(self):
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
            card (Room/Guest/Item): The object .
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
            card (Room/Guest/Item): The object .
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

