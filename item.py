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
        return self._name
    @name.setter
    def name(self, item_name):
        self._name = item_name

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, item_description):
        self._description = item_description

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

    def describe(self):
        """
        Prints the name of item and "is lying here".
        """
        print("The "+self._name + ' is lying here.')
