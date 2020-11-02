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










