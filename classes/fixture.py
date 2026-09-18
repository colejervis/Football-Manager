class Fixture:
    def __init__(self, fixture_id, homeClub, awayClub, leagueID, tournamentID, type, stage=None, date=None, score=None, leg=None, stadiumID = None):

        if fixture_id is not None:
            self.id = int(fixture_id)
        else:
            self.id = None

        self.homeClub = homeClub
        self.awayClub = awayClub
        self.date = date
        self.type = type
        self.stage = stage
        self.isCompleted = False
        self.homeScore = score
        self.awayScore = score
        self.homePenaltyScore = None
        self.awayPenaltyScore = None
        self.leg = leg
        self.stadiumID = stadiumID
        self.partnerFixture = None
        self.aggregateHomeScore = 0
        self.aggregateAwayScore = 0

        self.matchEvents = None
        self.matchStatistics = None
        self.matchForfeited = False

        if stadiumID is None:
            self.stadiumID = homeClub.getStadiumID()

        if leagueID is not None:
            self.leagueID = int(leagueID)
        else:
            self.leagueID = None

        if tournamentID is not None:
            self.tournamentID = int(tournamentID)
        else:
            self.tournamentID = None

        self.name = f"{self.homeClub.getName()} {self.awayClub.getName()}"

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def setPartnerFixture(self, partner):
        self.partnerFixture = partner

    def getPartnerFixture(self):
        return self.partnerFixture

    def setClubs(self, homeClub, awayClub):
        self.homeClub = homeClub
        self.awayClub = awayClub

    def getTeams(self):
        return self.homeClub, self.awayClub

    def setDate(self, date):
        self.date = date

    def getDate(self):
        return self.date

    def getLeagueID(self):
        return self.leagueID

    def getTournamentID(self):
        return self.tournamentID

    def getType(self):
        return self.type

    def getStage(self):
        return self.stage

    def getLeg(self):
        return self.leg

    def getStadiumID(self):
        return self.stadiumID

    def getScore(self):
        return self.homeScore, self.awayScore

    def getPenaltyScore(self):
        if self.homePenaltyScore is None and self.awayPenaltyScore is None:
            return None
        else:
            return self.homePenaltyScore, self.awayPenaltyScore

    def getAggregateScore(self):
        return self.aggregateHomeScore, self.aggregateAwayScore

    def setScore(self, homeScore, awayScore):
        self.homeScore = int(homeScore)
        self.awayScore = int(awayScore)

    def setPenaltyScore(self, homePenaltyScore, awayPenaltyScore):
        self.homePenaltyScore = int(homePenaltyScore)
        self.awayPenaltyScore = int(awayPenaltyScore)

    def updateAggregateScore(self, homeScore, awayScore):
        self.aggregateHomeScore = self.aggregateHomeScore + int(homeScore)
        self.aggregateAwayScore = self.aggregateAwayScore + int(awayScore)

    def addFixtureToClubLists(self):
        self.homeClub.addFixture(self)
        self.awayClub.addFixture(self)

    def getMatchEvents(self):
        return self.matchEvents
    def getMatchStatistics(self):
        return self.matchStatistics
    def setMatchEvents(self, matchEvents):
        self.matchEvents = matchEvents
    def setMatchStatistics(self, matchStatistics):
        self.matchStatistics = matchStatistics