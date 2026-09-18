import copy
import random
from registry import get_class

Fixture = get_class("Fixture")

class KnockoutTournament:

    ROUND_NAMES = {
        2: "Final",
        4: "Semi Final",
        8: "Quarter Final",
        16: "Round of 16",
        32: "Round of 32",
        64: "Round of 64"
    }

    def __init__(self, tournament_id, name, teams, DateObject, preferred_matchday, parentLeagueID = None, rules = None):

        if tournament_id is not None:
            self.id = int(tournament_id)
        else:
            self.id = None

        self.name = name
        self.teams = teams
        self.DateObject = DateObject
        self.preferred_matchday = preferred_matchday
        self.currentRound = None
        self.currentRoundTwoLegged = False
        self.currentRoundFixtures = []
        self.currentRoundTeams = teams
        self.nextRoundTeams = []
        self.parentLeagueID = parentLeagueID
        self.rules = rules

        size = self.getTournamentSize()
        self.addByes(size)
        self.buildRound()

        self.winner = None

    def getLeagueID(self):
        return None

    def getName(self):
        return self.name

    def getWinner(self):
        return self.winner

    def getTournamentSize(self):
        size = 1

        # ENSURES SIZE IS ONLY 2, 4, 8, 16, 32 ETC
        while size < len(self.teams):
            size *= 2

        return size

    def addByes(self, size):
        # IF UNNATURAL NUMBER OF TEAMS, ADD 'BYES' USING NONE VALUES
        while len(self.teams) < size:
            self.teams.append(None)

    def buildRound(self):

        # Checks if there is a winner
        if len(self.currentRoundTeams) == 1:
            self.winner = self.currentRoundTeams[0]
            return

        self.currentRound = KnockoutTournament.ROUND_NAMES[len(self.currentRoundTeams)]

        # Goes to preferred Weekday of tournament if not already, and advances a week for next round of fixtures
        while self.DateObject.getWeekday() != self.preferred_matchday:
            self.DateObject.advance()
        for i in range(7):
            self.DateObject.advance()

        self.currentRoundTwoLegged = False
        # Checks if round should be two legged
        if self.currentRound == "Semi Final" and "two_legged_semi_final" in self.rules.keys():
            self.currentRoundTwoLegged = True
            tempDate = copy.deepcopy(self.DateObject)
            for i in range(7):
                tempDate.advance()
            second_leg_date = tempDate.getDate()
        else:
            leg = None

        # Checks if is final and  if designated venue is set
        if self.currentRound == "Final" and "final_stadium_id" in self.rules.keys():
            stadiumID = self.rules["final_stadium_id"]
        else:
            stadiumID = None

        for i in range(0, len(self.currentRoundTeams), 2): # ITERATES EVERY OTHER TEAM (EACH FIXTURE CONTAINS TWO TEAMS)

            if self.currentRoundTwoLegged:
                leg = 1

            f = Fixture(None, self.currentRoundTeams[i], self.currentRoundTeams[i + 1], None, self.id,
                        "knockout", self.currentRound, self.DateObject.getDate(), None, leg, stadiumID)
            self.currentRoundFixtures.append(f)
            f.addFixtureToClubLists()

            if self.currentRoundTwoLegged:
                leg = leg + 1
                f2 = Fixture(None, self.currentRoundTeams[i + 1], self.currentRoundTeams[i], None, self.id,
                             "knockout", self.currentRound, second_leg_date, None, leg, stadiumID)
                f.setPartnerFixture(f2)
                f2.setPartnerFixture(f)
                self.currentRoundFixtures.append(f2)
                f2.addFixtureToClubLists()

    def postMatchProcessing(self, fixture):
        homeTeam, awayTeam = fixture.getTeams()

        if self.currentRoundTwoLegged and fixture.getLeg() == 2:
            firstLeg = fixture.getPartnerFixture()
            firstLegHomeScore, firstLegAwayScore = firstLeg.getScore()
            secondLegHomeScore, secondLegAwayScore = fixture.getScore()

            if fixture.getPenaltyScore() is not None:
                homePens, awayPens = fixture.getPenaltyScore()

            aggHome = firstLegAwayScore + secondLegHomeScore
            aggAway = firstLegHomeScore + secondLegAwayScore

            if aggHome > aggAway:
                self.nextRoundTeams.append(homeTeam)
            elif aggHome < aggAway:
                self.nextRoundTeams.append(awayTeam)
            elif homePens > awayPens:
                self.nextRoundTeams.append(homeTeam)
            elif homePens < awayPens:
                self.nextRoundTeams.append(awayTeam)

        elif not self.currentRoundTwoLegged:
            homeScore, awayScore = fixture.getScore()

            if fixture.getPenaltyScore() is not None:
                homePens, awayPens = fixture.getPenaltyScore()

            if homeScore > awayScore:
                self.nextRoundTeams.append(homeTeam)
            elif awayScore > homeScore:
                self.nextRoundTeams.append(awayTeam)
            elif homePens > awayPens:
                self.nextRoundTeams.append(homeTeam)
            elif homePens < awayPens:
                self.nextRoundTeams.append(awayTeam)

        if self.roundChecker():
            self.updateRound()
            self.buildRound()

    def roundChecker(self):
        passed = True
        for fixture in self.currentRoundFixtures:
            if fixture.isCompleted is False:
                passed = False

        return passed

    def updateRound(self):
        self.currentRoundTeams = self.nextRoundTeams
        self.nextRoundTeams = []
        self.currentRoundFixtures = []

