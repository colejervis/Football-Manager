class Nation:
    def __init__(self, nation_id, name, abbreviation, reputation):
        self.id = int(nation_id)
        self.name = name
        self.abbreviation = abbreviation
        self.reputation = int(reputation)
    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def getAbbreviation(self):
        return self.abbreviation
    def getReputation(self):
        return self.reputation