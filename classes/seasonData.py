class PlayerSeasonData:

    def __init__(self, clubID = None):
        self.clubID = clubID
        self.appearances = 0
        self.subAppearances = 0
        self.goals = 0
        self.assists = 0
        self.yellowCards = 0
        self.redCards = 0
        self.cleanSheets = 0

class ClubSeasonData:

    def __init__(self):
        self.matchesPlayed = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.cleanSheets = 0
        self.totalPossession = 0
        self.totalPasses = 0
        self.totalShots = 0
        self.totalBigChances = 0
        self.totalXG = 0
        self.totalFouls = 0
        self.totalYellowCards = 0
        self.totalRedCards = 0

    def getPoints(self):
        return (self.wins * 3) + self.draws

    def getGoalDifference(self):
        return self.goalsFor - self.goalsAgainst