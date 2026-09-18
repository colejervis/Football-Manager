class FreeAgents:

    COLOR_MAPPING = {
        "black": "⚫",
        "white": "⚪",
    }

    def __init__(self, club_id, full_name, short_name):
        self.id = club_id
        self.full_name = full_name
        self.short_name = short_name
        self.players = []
        self.first_team = []
        self.youth_team = []
        self.managers = []
        self.fixtures = []
        self.reputation = 0
        self.primary_color = "black"
        self.secondary_color = "white"

    def getID(self):
        return self.id

    def getFullName(self):
        return self.full_name

    def getShortName(self):
        return self.short_name

    def getName(self):
        return self.full_name

    def addPlayer(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players

    def getFirstTeam(self):
        return self.first_team

    def getYouthTeam(self):
        return self.youth_team

    def addManager(self, manager):
        self.managers.append(manager)

    def getManagers(self):
        return self.managers

    def getLeagueID(self):
        return None

    def getNationID(self):
        return None

    def getReputation(self):
        return self.reputation

    def printColors(self):
        return f"{self.COLOR_MAPPING[self.primary_color]}{self.COLOR_MAPPING[self.secondary_color]}"

    def getFixtures(self):
        return self.fixtures