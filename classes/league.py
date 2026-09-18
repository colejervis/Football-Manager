import random
from registry import get_class

Fixture = get_class("Fixture")
KnockoutTournament = get_class("KnockoutTournament")

class League:
    def __init__(self, league_id, nationID, name, reputation, start_date, promotion_places, leagueAboveID, playoff_qualifying_positions, relegation_places, leagueBelowID):
        self.id = int(league_id)
        self.nationID = int(nationID)
        self.name = name
        self.reputation = int(reputation)
        self.clubs = {}
        self.fixtures = []
        self.start_date = start_date
        self.promotion_places = int(promotion_places)
        self.playoff_qualifying_positions = playoff_qualifying_positions
        self.relegation_places = int(relegation_places)
        self.leagueAboveID = int(leagueAboveID)
        self.leagueBelowID = int(leagueBelowID)
        self.playoffObject = None

        self.playoffTeams = []
        self.playoffsArranged = False

    def getLeagueID(self):
        return self.id

    def getTournamentID(self):
        return None

    def getLeagueAboveID(self):
        return self.leagueAboveID

    def getLeagueBelowID(self):
        return self.leagueBelowID

    def getNationID(self):
        return self.nationID

    def getName(self):
        return self.name

    def addClub(self, id, club):
        self.clubs[id] = club

    def removeClub(self, id):
        del self.clubs[id]

    def getClubs(self):
        return self.clubs

    def getFixtures(self):
        return self.fixtures

    def getPromotionPlaces(self):
        return self.promotion_places

    def getRelegationPlaces(self):
        return self.relegation_places

    def getPlayoffFixtures(self):
        return self.playoffFixtures

    def getReputation(self):
        return self.reputation

    def getPlayoffQualifyingPositions(self):
        return self.playoff_qualifying_positions

    def updateStartDate(self, current_date):
        cDay, cMonth, cYear = current_date
        sDay, sMonth, sYear = self.start_date.split("/")

        self.start_date = f"{sDay}/{sMonth}/{cYear}"

    def arrangeFixtures(self, DateObject):

        """
        1 - Gets the league's start date from the league object, and finds next available saturday
        2 - Generates all possible fixtures in the league by cycling through all teams and in another inner loop, selects the other clubs in the league. If
        the fixture doesn't already exist, it is added to the league's fixtures list.
        3 - It finds the number of match days, and starts adding fixtures into the match day so that each team only plays once on that match day.
        4 - If it gets past a certain day late in the season and there are still unscheduled match days, it will 'back-track' to early on in the season and
        schedule matches to happen on Tuesday nights every 28 days.
        """

        if self.id == 0:
            return


        # FINDS NEXT SATURDAY

        start_date = self.start_date
        match_date = None

        if match_date is None:

            match_date = start_date
            day, month, year = match_date.split("/")
            day = int(day)
            month = int(month)
            year = int(year)

            DateObject.setDate(day, month, year)
            while DateObject.getWeekday() != "Saturday":
                DateObject.advance()

        # GENERATES ALL POSSIBLE FIXTURES FOR EVERY TEAM IN LEAGUE

        id = 0
        fixtures = []

        for club in self.clubs.values():
            for secondClub in self.clubs.values():
                if club != secondClub:
                    duplicate = False
                    # Check for duplicates, if none allow code below

                    for fixture in fixtures:

                        home, away = fixture.getTeams()
                        if club == home and secondClub == away:
                            duplicate = True

                    if not duplicate:
                        id = id + 1
                        f = Fixture(id, club, secondClub, self.id, None, "league")
                        fixtures.append(f)

        amount_of_fixtures = len(fixtures)

        # SPLITS INTO SEPARATE MATCH DAYS AND FINDS AVAILABLE DAY, while loop needed as in some cases, algorithm breaks when not shuffled correctly

        matchdays_count = 2 * (len(self.clubs) - 1)

        while len(self.fixtures) < amount_of_fixtures:

            random.shuffle(fixtures)

            back_track_completed = False

            for i in range(matchdays_count):

                # BACK TRACKS TO FILL IN MID-WEEK FIXTURES IF IT GETS PAST 15TH MAY
                day, month, year = DateObject.getDate()
                sDay, sMonth, sYear = self.start_date.split("/")

                if day > 10 and month >= 5 and year > int(sYear) and back_track_completed == False:
                    DateObject.setDate(15, 9, year-1)
                    # Finds next Tuesday
                    while DateObject.getWeekday() != "Tuesday":
                        DateObject.advance()
                    back_track_completed = True


                matchday = []
                used_teams = set()

                fixtures_to_remove = []
                for fixture in fixtures:
                    home, away = fixture.getTeams()
                    if (home not in used_teams) and (away not in used_teams):
                        used_teams.add(home)
                        used_teams.add(away)
                        fixtures_to_remove.append(fixture)
                        matchday.append(fixture)

                for fixture in fixtures_to_remove:
                    fixtures.remove(fixture)

                if not back_track_completed:
                    for i in range(7):
                        DateObject.advance()
                    match_date = DateObject.getDate()
                else:
                    for i in range(28): # Sets midweek fixtures to happen every month
                        DateObject.advance()
                    match_date = DateObject.getDate()

                for index, fixture in enumerate(matchday):
                    fixture.setDate(match_date)

                for fixture in matchday:
                    self.fixtures.append(fixture)

        # ENSURES FIXTURES LIST IS IN ORDER
        match_date = start_date
        day, month, year = match_date.split("/")
        day = int(day)
        month = int(month)
        year = int(year)
        fixtures = self.fixtures
        self.fixtures = []

        DateObject.setDate(day, month, year)
        for i in range(365):
            DateObject.advance()
            for fixture in fixtures:
                if fixture.getDate() == DateObject.getDate():
                    self.fixtures.append(fixture)


        # ADDS FIXTURES TO CLUB'S FIXTURE LIST
        for fixture in self.fixtures:
            fixture.addFixtureToClubLists()

    def getPlayoffObject(self):
        return self.playoffObject

    def postMatchProcessing(self, fixture):

        homeTeam, awayTeam = fixture.getTeams()
        leagueID = fixture.getLeagueID()

        # GET MATCH SCORE
        homeScore, awayScore = fixture.getScore()

        # GET SEASON DATA OBJECTS
        homeClubLeagueDataObject = homeTeam.getSeasonData(leagueID)
        awayClubLeagueDataObject = awayTeam.getSeasonData(leagueID)

        homeClubLeagueDataObject.matchesPlayed += 1
        awayClubLeagueDataObject.matchesPlayed += 1
        homeClubLeagueDataObject.goalsFor += homeScore
        homeClubLeagueDataObject.goalsAgainst += awayScore
        awayClubLeagueDataObject.goalsFor += awayScore
        awayClubLeagueDataObject.goalsAgainst += homeScore

        if homeScore == awayScore:
            homeClubLeagueDataObject.draws += 1
            awayClubLeagueDataObject.draws += 1
        elif homeScore > awayScore:
            homeClubLeagueDataObject.wins += 1
            awayClubLeagueDataObject.losses += 1
        else:
            homeClubLeagueDataObject.losses += 1
            awayClubLeagueDataObject.wins += 1

        if awayScore == 0:
            homeClubLeagueDataObject.cleanSheets += 1
        if homeScore == 0:
            awayClubLeagueDataObject.cleanSheets += 1

        statistics = fixture.getMatchStatistics()


        homeClubLeagueDataObject.totalPossession += statistics["homePossession"]
        awayClubLeagueDataObject.totalPossession += statistics["awayPossession"]
        homeClubLeagueDataObject.totalPasses += statistics["homePasses"]
        awayClubLeagueDataObject.totalPasses += statistics["awayPasses"]
        homeClubLeagueDataObject.totalShots += statistics["homeShots"]
        awayClubLeagueDataObject.totalShots += statistics["awayShots"]
        homeClubLeagueDataObject.totalBigChances += statistics["homeBigChances"]
        awayClubLeagueDataObject.totalBigChances += statistics["awayBigChances"]
        homeClubLeagueDataObject.totalXG += statistics["homeXG"]
        awayClubLeagueDataObject.totalXG += statistics["awayXG"]
        homeClubLeagueDataObject.totalFouls += statistics["homeFouls"]
        awayClubLeagueDataObject.totalFouls += statistics["awayFouls"]
        homeClubLeagueDataObject.totalYellowCards += statistics["homeYellowCards"]
        awayClubLeagueDataObject.totalYellowCards += statistics["awayYellowCards"]
        homeClubLeagueDataObject.totalRedCards += statistics["homeRedCards"]
        awayClubLeagueDataObject.totalRedCards += statistics["awayRedCards"]


    def arrangePlayoffs(self, DateObject, game):
        if self.playoff_qualifying_positions == 0:
            return

        self.playoffTeams = []
        playoff_qualifying_positions = str(self.playoff_qualifying_positions)
        first_team_position = int(playoff_qualifying_positions[0])
        last_team_position = int(playoff_qualifying_positions[1])

        clubList = []
        for club in self.clubs.values():
            clubList.append(club)

        clubList.sort(key=lambda club: (club.getSeasonData(self.id).getPoints(), club.getSeasonData(self.id).getGoalDifference(), club.getSeasonData(self.id).goalsFor), reverse=True)
        teams = []
        top_pointer = first_team_position - 1
        bottom_pointer = last_team_position - 1

        while top_pointer < bottom_pointer:
            teams.append(clubList[top_pointer])
            teams.append(clubList[bottom_pointer])
            top_pointer += 1
            bottom_pointer -= 1

        preferred_matchday = "Saturday"

        rules = {
            "two_legged_semi_final": True,
            "final_stadium_id": 1000,
        }

        tournamentID = 100000 + self.id
        self.playoffObject = KnockoutTournament(tournamentID, f"{self.name} Playoffs", teams, DateObject, preferred_matchday, self.id, rules)
        game.getTournaments()[tournamentID] = self.playoffObject