class Position:
    def __init__(self, position_id, abbreviation, name):
        self.id = int(position_id)
        self.abbreviation = abbreviation
        self.name = name

    def __str__(self):
        return self.abbreviation

    def getID(self):
        return self.id
    def getAbbreviation(self):
        return self.abbreviation
    def getName(self):
        return self.name