from time import process_time

from gamelogic import *

import random
import copy


class gameObject:
    def __init__(self, dateObject, players, positions, clubs, leagues, managers, stadiums, nations):
        self.dateObject = dateObject
        self.players = players
        self.positions = positions
        self.clubs = clubs
        self.leagues = leagues
        self.managers = managers
        self.stadiums = stadiums
        self.nations = nations

        self.playoffsArranged = False

        self.onHoliday = False
        self.holidayDate = None

    def getAll(self):
        return self.dateObject, self.players, self.positions, self.clubs, self.leagues, self.managers, self.stadiums, self.nations


    def annualUpdate(self):
        for player in self.players.values():
            # REMOVING LOANS
            if player.getParentClub() != player.getClub():

                parentClubObject = self.clubs[player.getParentClub()]
                loanClubObject = self.clubs[player.getLoanClub()]

                player.setClub(player.getParentClub())
                if player in loanClubObject.getPlayers():
                    # Removes player from loan club
                    loanClubObject.getPlayers().remove(player)
                    # Adds them back to parent club roster
                    parentClubObject.getPlayers().append(player)

                player.setLoanClub(None)

            # PLAYER CONTRACT LENGTH DECREASE
            if player.getContractLength() > 0:
                player.decrementContractLength()

            # HANDLING CONTRACT EXPIRY PLAYERS
            if player.getContractLength() == 0:
                clubObject = self.clubs[player.getClub()]
                if player in clubObject.getPlayers():
                    # Removes player from club
                    clubObject.getPlayers().remove(player)

                # Adds player to Free Agents
                player.setClub(0)
                player.setParentClub(0)
                player.setLoanClub(None)
                self.clubs[0].getPlayers().append(player)

        for manager in self.managers.values():
            # INCREMENTING PLAYER AGES BY 1
            manager.incrementAge()

        # SPLITS CLUB PLAYERS INTO FIRST TEAM AND YOUTH ACADEMY

        for club in self.clubs.values():
            if club.getID() != 0:
                club.autoSplitPlayers(self.dateObject)

    def seasonUpdate(self):

        # PROMOTION / RELEGATION LOGIC HERE

        for league in self.leagues.values():

            clubs = league.getClubs()
            clubList = []

            for club in clubs.values():
                clubList.append(club)

            clubList.sort(key=lambda club: (-club.getPoints(), -club.getGoalDifference(), -club.getGoalsFor(), club.getFullName()))

            promoted = []
            relegated = []

            for i in range(league.getPromotionPlaces()):
                promoted.append(clubList[i])

            if league.getPlayoffObject() is not None:
                playoffWinner = league.getPlayoffObject().getWinner()
                promoted.append(playoffWinner)

            clubList.reverse()

            for i in range(league.getRelegationPlaces()):
                relegated.append(clubList[i])

            if league.getLeagueAboveID() != 0:
                for club in promoted:
                    club.setLeague(league.getLeagueAboveID())
                    league.removeClub(club.getID())
                    self.leagues[league.getLeagueAboveID()].addClub(club.getID(), club)

            if league.getLeagueBelowID() != 0:
                for club in relegated:
                    club.setLeague(league.getLeagueBelowID())
                    league.removeClub(club.getID())
                    self.leagues[league.getLeagueBelowID()].addClub(club.getID(), club)



        # REMOVES ALL LEAGUE TABLE DATA FROM CLUBS
        for club in self.clubs.values():
            club.clearSeasonData()

        # FIXTURE ARRANGEMENT

        for league in self.leagues.values():
            league.getFixtures().clear()

        for club in self.clubs.values():
            club.getFixtures().clear()

        for league in self.leagues.values():
            league.updateStartDate(self.dateObject.getDate())
            tempDate = copy.deepcopy(self.dateObject)
            league.arrangeFixtures(tempDate)

        self.playoffsArranged = False

    def morningDailyUpdate(self):

        # CHECKS IF SEASONS HAVE FINISHED TO ARRANGE PLAYOFFS
        day, month, year = self.dateObject.getDate()
        if day > 20 and month == 5 and self.playoffsArranged is False:
            for league in self.leagues.values():
                tempDate = copy.deepcopy(self.dateObject)
                league.arrangePlayoffs(tempDate)
                self.playoffsArranged = True

    def afternoonDailyUpdate(self):
        match_checker(self)
        self.dateObject.advance()


    def getDateObject(self):
        return self.dateObject

    def getPlayers(self):
        return self.players

    def getPositions(self):
        return self.positions

    def getClubs(self):
        return self.clubs

    def getLeagues(self):
        return self.leagues

    def getManagers(self):
        return self.managers

    def getStadiums(self):
        return self.stadiums

    def getNations(self):
        return self.nations


    def arrangeHoliday(self, day, month, year):
        self.onHoliday = True
        self.holidayDate = day, month, year

    def endHoliday(self):
        self.onHoliday = False
        self.holidayDate = None

    def getHolidayDate(self):
        return self.holidayDate

    def getHolidayStatus(self):
        return self.onHoliday


class Date:
    daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self):
        self.day = 0
        self.month = 0
        self.year = 0

    def setDate(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def getDate(self):
        return self.day, self.month, self.year

    def getYear(self):
        return self.year

    def isLeapYear(self):
        return (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0)

    def days_in_february(self):
        if self.month == 2:
            if self.isLeapYear() == True:
                return 29
            else:
                return 28

    # USED IN HOLIDAY MENU TO CHECK IF PROPOSED DATE IS VALID
    def validDateChecker(self, day, month, year):
        if day > Date.daysInMonth[month - 1]:
            return False
        else:
            return True

    def isInFutureChecker(self, day, month, year):

        if year > self.year:
            return True
        elif year < self.year:
            return False
        else:
            if month > self.month:
                return True
            elif month < self.month:
                return False
            else:
                if day > self.day:
                    return True
                elif day < self.day:
                    return False
                elif day == self.day:
                    return False


    def advance(self):
        Date.daysInMonth[1] = Date.days_in_february(self)

        if self.day == Date.daysInMonth[self.month - 1] and self.month == 12:
            self.month = 1
            self.day = 1
            self.year += 1

        elif self.day == Date.daysInMonth[self.month - 1] and self.month != 12:
            self.month += 1
            self.day = 1
        else:
            self.day += 1

    # USING ZELLER'S CONGRUENCE:
    def getWeekday(self):

        q = self.day
        m = self.month
        y = self.year

        # Adjust months to match formula - Jan & Feb become 13, 14 of previous year
        if m == 1 or m == 2:
            m += 12
            y -= 1

        K = y % 100  # year of the century
        J = y // 100  # zero-based century

        h = (q + (13 * (m + 1)) // 5 + K + (K // 4) + (J // 4) + (5 * J)) % 7

        # Map result to weekday names
        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return days[h]

class Nation:
    def __init__(self, id, name, abbreviation, reputation):
        self.id = int(id)
        self.name = name
        self.abbreviation = abbreviation
        self.reputation = int(reputation)
    def getName(self):
        return self.name
    def getAbbreviation(self):
        return self.abbreviation
    def getReputation(self):
        return self.reputation



class Person:
    def __init__(self, id, firstname, surname, age, nationality):
        self.id = int(id)
        self.firstname = firstname
        self.surname = surname
        self.age = int(age)
        self.nationality = int(nationality)

    def getAge(self):
        return self.age

    def incrementAge(self):
        self.age = self.age + 1

    def getNationality(self):
        return self.nationality

    def setNation(self, nation):
        self.nationality = nation

    def getSurname(self):
        return  self.surname


class Stadium:
    def __init__(self, id, name, clubID, capacity, opened_date, city):
        self.id = int(id)
        self.name = name
        self.clubID = int(clubID)
        self.capacity = capacity
        self.opened_date = opened_date
        self.city = city

    def getID(self):
        return self.id

    def getClub(self):
        return self.clubID

    def getName(self):
        return self.name

    def getCapacity(self):
        return self.capacity

    def getOpenedDate(self):
        return self.opened_date

    def getCity(self):
        return self.city


class Manager(Person):
    def __init__(self, id, firstname, surname, age, nationality, clubID, preferred_formation):
        Person.__init__(self, id, firstname, surname, age, nationality)
        self.clubID = int(clubID)
        self.preferred_formation = preferred_formation

    def getPreferredFormation(self):
        return self.preferred_formation

    def getName(self):
        return self.firstname + " " + self.surname

    def getClub(self):
        return self.clubID

    def setClub(self, newID):
        self.clubID = newID

    def getID(self):
        return self.id


class PlayerManager(Person):
    def __init__(self, id, firstname, surname, age, nationality, clubID):
        super().__init__(id, firstname, surname, age, nationality)
        self.id = int(id)
        self.firstname = firstname
        self.surname = surname
        self.age = int(age)
        self.nationality = int(nationality)
        self.clubID = int(clubID)

        self.playerShortlist = []

        self.preferred_formation = "4231"

    def getPreferredFormation(self):
        return self.preferred_formation

    def getName(self):
        return self.firstname + " " + self.surname

    def getClub(self):
        return self.clubID

    def setClub(self, newID):
        self.clubID = newID

    def getID(self):
        return self.id

    def getShortlist(self):
        return self.playerShortlist

    def shortlistAdd(self, player):
        self.playerShortlist.append(player)

    def shortlistRemove(self, player):
        self.playerShortlist.remove(player)

class League:
    def __init__(self, id, nationID, name, reputation, start_date, promotion_places, leagueAboveID, playoff_qualifying_positions, relegation_places, leagueBelowID):
        self.id = int(id)
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

    def getLeagueID(self):
        return self.id

    def getLeagueAboveID(self):
        return self.leagueAboveID

    def getLeagueBelowID(self):
        return self.leagueBelowID

    def getNation(self):
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
                    for i in range(21): # Sets midweek fixtures to happen every third week
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
        if fixture.getType() == "league":
            # POST MATCH PROCESSING FOR LEAGUE MATCHES

            homeClub, awayClub = fixture.getTeams()
            homeScore, awayScore = fixture.getScore()
            homeClub.incrementMatchesPlayed()
            awayClub.incrementMatchesPlayed()
            for i in range(homeScore):
                homeClub.incrementGoalsFor()
                awayClub.incrementGoalsAgainst()
            for i in range(awayScore):
                awayClub.incrementGoalsFor()
                homeClub.incrementGoalsAgainst()
            if homeScore == awayScore:
                homeClub.incrementDraws()
                awayClub.incrementDraws()
            elif homeScore > awayScore:
                homeClub.incrementWins()
                awayClub.incrementLosses()
            elif homeScore < awayScore:
                awayClub.incrementWins()
                homeClub.incrementLosses()

        elif fixture.getType() == "knockout": # PLAYOFF MATCH PROCESSING
            self.playoffObject.postMatchProcessing(fixture)

    def arrangePlayoffs(self, DateObject):
        if self.playoff_qualifying_positions == str(0):
            return

        self.playoffTeams = []
        first_team_position = int(self.playoff_qualifying_positions[0])
        last_team_position = int(self.playoff_qualifying_positions[1])

        clubList = []
        for club in self.clubs.values():
            clubList.append(club)

        clubList.sort(key=lambda club: (club.getPoints(), club.getGoalDifference()), reverse=True)
        teams = []
        pointer = first_team_position - 1
        numberOfTeams = (last_team_position - first_team_position) + 1

        for i in range(numberOfTeams):
            teams.append(clubList[pointer])
            pointer = pointer + 1

        preferred_matchday = "Saturday"

        self.playoffObject = knockoutTournament(None, f"{self.name} Playoffs", teams, DateObject, preferred_matchday, self.id)


class knockoutTournament:

    ROUND_NAMES = {
        2: "Final",
        4: "Semi Final",
        8: "Quarter Final",
        16: "Round of 16",
        32: "Round of 32",
        64: "Round of 64"
    }

    def __init__(self, id, name, teams, DateObject, preferred_matchday, parentLeagueID = None):

        self.id = id
        self.name = name
        self.teams = teams
        self.DateObject = DateObject
        self.preferred_matchday = preferred_matchday
        self.currentRound = None
        self.currentRoundFixtures = []
        self.currentRoundTeams = teams
        self.nextRoundTeams = []
        self.parentLeagueID = parentLeagueID

        size = self.getTournamentSize()
        self.addByes(size)
        self.buildRound()

        self.winner = None

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

        self.currentRound = knockoutTournament.ROUND_NAMES[len(self.currentRoundTeams)]

        # Goes to preferred Weekday of tournament if not already, and advances a week for next round of fixtures
        while self.DateObject.getWeekday() != self.preferred_matchday:
            self.DateObject.advance()
        for i in range(7):
            self.DateObject.advance()

        for i in range(0, len(self.currentRoundTeams), 2): # ITERATES EVERY OTHER TEAM (EACH FIXTURE CONTAINS TWO TEAMS)
            f = Fixture(None, self.currentRoundTeams[i], self.currentRoundTeams[i+1], self.parentLeagueID, None, "knockout", self.currentRound, self.DateObject.getDate())
            self.currentRoundFixtures.append(f)
            f.addFixtureToClubLists()


    def postMatchProcessing(self, fixture):
        homeScore, awayScore = fixture.getScore()
        homeTeam, awayTeam = fixture.getTeams()
        if homeScore > awayScore:
            self.nextRoundTeams.append(homeTeam)
        elif awayScore > homeScore:
            self.nextRoundTeams.append(awayTeam)

        if self.roundChecker():
            self.updateRound()
            self.buildRound()

    def roundChecker(self):
        passed = True
        for fixture in self.currentRoundFixtures:
            if fixture.getScore() is None:
                passed = False

        return passed

    def updateRound(self):
        self.currentRoundTeams = self.nextRoundTeams
        self.nextRoundTeams = []
        self.currentRoundFixtures = []




class Fixture:
    def __init__(self, id, homeClub, awayClub, leagueID, tournamentID, type, stage=None, date=None, score=None):

        if id is not None:
            self.id = int(id)

        self.homeClub = homeClub
        self.awayClub = awayClub
        self.date = date
        self.type = type
        self.stage = stage
        self.homeScore = score
        self.awayScore = score

        self.leagueID = int(leagueID)

        if tournamentID is not None:
            self.tournamentID = int(tournamentID)
        else:
            self.tournamentID = None

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

    def getScore(self):
        if self.homeScore is None and self.awayScore is None:
            return None
        else:
            return self.homeScore, self.awayScore

    def setScore(self, homeScore, awayScore):
        self.homeScore = int(homeScore)
        self.awayScore = int(awayScore)

    def addFixtureToClubLists(self):
        self.homeClub.addFixture(self)
        self.awayClub.addFixture(self)

class Player:

    GOALKEEPER_WEIGHTS = {
        "passing": 0.01,
        "dribbling": 0.00,
        "finishing": 0.00,
        "defending": 0.01,
        "ball_control": 0.01,
        "delivery": 0.00,
        "vision": 0.01,
        "football_iq": 0.02,
        "positioning": 0.02,
        "composure": 0.04,
        "decision_making": 0.04,
        "work_rate": 0.01,
        "aggression": 0.01,
        "pace": 0.01,
        "strength": 0.02,
        "aerial": 000,
        "stamina": 0.00,
        "shot_stopping": 0.32,
        "handling": 0.20,
        "distribution": 0.12,
        "command": 0.12
    }

    CENTREBACK_WEIGHTINGS = {
        "passing": 0.03,
        "dribbling": 0.01,
        "finishing": 0.00,
        "defending": 0.20,
        "ball_control": 0.03,
        "delivery": 0.00,
        "vision": 0.02,
        "football_iq": 0.00,
        "positioning": 0.15,
        "composure": 0.06,
        "decision_making": 0.06,
        "work_rate": 0.03,
        "aggression": 0.06,
        "pace": 0.07,
        "strength": 0.12,
        "aerial": 0.14,
        "stamina": 0.02,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }

    FULLBACK_WEIGHTINGS = {
        "passing": 0.08,
        "dribbling": 0.07,
        "finishing": 0.01,
        "defending": 0.16,
        "ball_control": 0.05,
        "delivery": 0.10,
        "vision": 0.04,
        "football_iq": 0.05,
        "positioning": 0.09,
        "composure": 0.04,
        "decision_making": 0.05,
        "work_rate": 0.07,
        "aggression": 0.02,
        "pace": 0.09,
        "strength": 0.03,
        "aerial": 0.02,
        "stamina": 0.03,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }

    DEFENSIVE_MIDFIELDER_WEIGHTINGS = {
        "passing": 0.09,
        "dribbling": 0.02,
        "finishing": 0.00,
        "defending": 0.16,
        "ball_control": 0.06,
        "delivery": 0.02,
        "vision": 0.06,
        "football_iq": 0.08,
        "positioning": 0.11,
        "composure": 0.06,
        "decision_making": 0.08,
        "work_rate": 0.08,
        "aggression": 0.05,
        "pace": 0.04,
        "strength": 0.05,
        "aerial": 0.05,
        "stamina": 0.07,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }

    CENTRAL_MIDFIELDER_WEIGHTINGS = {
        "passing": 0.12,
        "dribbling": 0.06,
        "finishing": 0.02,
        "defending": 0.05,
        "ball_control": 0.10,
        "delivery": 0.02,
        "vision": 0.10,
        "football_iq": 0.09,
        "positioning": 0.04,
        "composure": 0.05,
        "decision_making": 0.10,
        "work_rate": 0.10,
        "aggression": 0.02,
        "pace": 0.04,
        "strength": 0.03,
        "aerial": 0.01,
        "stamina": 0.05,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }

    ATTACKING_MIDFIELDER_WEIGHTINGS = {
        "passing": 0.11,
        "dribbling": 0.10,
        "finishing": 0.07,
        "defending": 0.01,
        "ball_control": 0.10,
        "delivery": 0.04,
        "vision": 0.15,
        "football_iq": 0.09,
        "positioning": 0.01,
        "composure": 0.10,
        "decision_making": 0.11,
        "work_rate": 0.04,
        "aggression": 0.01,
        "pace": 0.05,
        "strength": 0.01,
        "aerial": 0.00,
        "stamina": 0.02,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }

    WINGER_WEIGHTINGS = {
        "passing": 0.06,
        "dribbling": 0.16,
        "finishing": 0.08,
        "defending": 0.01,
        "ball_control": 0.10,
        "delivery": 0.10,
        "vision": 0.05,
        "football_iq": 0.07,
        "positioning": 0.01,
        "composure": 0.04,
        "decision_making": 0.06,
        "work_rate": 0.04,
        "aggression": 0.01,
        "pace": 0.17,
        "strength": 0.01,
        "aerial": 0.01,
        "stamina": 0.02,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }
    STRIKER_WEIGHTINGS = {
        "passing": 0.01,
        "dribbling": 0.05,
        "finishing": 0.19,
        "defending": 0.00,
        "ball_control": 0.06,
        "delivery": 0.00,
        "vision": 0.01,
        "football_iq": 0.13,
        "positioning": 0.00,
        "composure": 0.14,
        "decision_making": 0.08,
        "work_rate": 0.03,
        "aggression": 0.03,
        "pace": 0.12,
        "strength": 0.07,
        "aerial": 0.11,
        "stamina": 0.02,
        "shot_stopping": 0,
        "handling": 0,
        "distribution": 0,
        "command": 0
    }

    SECONDARY_POSITION_FAMILIARITY = 0.9

    secondary_position_mapping = {
        1: [],
        2: [],
        4: [],
        3: [2, 4],
        6: [5, 7],
        5: [6],
        7: [6],
        9: [8, 4],
        8: [9, 2],
        10: [],
    }

    def __init__(self, id, firstname, surname, birthDay, birthMonth, birthYear, nationality, clubID, position,
                 passing, dribbling, finishing, defending, ball_control, delivery,
                 vision, football_iq, positioning, composure, decision_making, work_rate, aggression,
                 pace, strength, stamina, aerial, shot_stopping, handling, distribution, command,
                 potential, height, current_wage, contract_length):
        self.id = int(id)
        self.firstname = firstname
        self.surname = surname
        self.birthDay = int(birthDay)
        self.birthMonth = int(birthMonth)
        self.birthYear = int(birthYear)
        self.nationality = int(nationality)
        self.clubID = int(clubID)
        self.parentClubID = int(clubID)
        self.loanClubID = None
        self.position = int(position)
        self.passing = int(passing)
        self.dribbling = int(dribbling)
        self.finishing = int(finishing)
        self.defending = int(defending)
        self.ball_control = int(ball_control)
        self.delivery = int(delivery)
        self.vision = int(vision)
        self.football_iq = int(football_iq)
        self.positioning = int(positioning)
        self.composure = int(composure)
        self.decision_making = int(decision_making)
        self.work_rate = int(work_rate)
        self.aggression = int(aggression)
        self.pace = int(pace)
        self.strength = int(strength)
        self.stamina = int(stamina)
        self.aerial = int(aerial)
        self.shot_stopping = int(shot_stopping)
        self.handling = int(handling)
        self.distribution = int(distribution)
        self.command = int(command)
        self.potential = int(potential)
        self.height = int(height)
        self.current_wage = int(current_wage)
        self.contract_length = int(contract_length)

    def calculateMarketValue(self, game):

        clubs = game.getClubs()
        leagues = game.getLeagues()
        nations = game.getNations()

        # SETS MARKET VALUE TO 0 IF PLAYER IS FREE AGENT
        if self.clubID == 0:
            return 0

        DateObject = game.getDateObject()
        age = self.getAge(DateObject)

        age_factor_mapping = {
            1: 1.2,
            21: 1.1,
            25: 1.05,
            28: 1.0,
            31: 0.9,
            33: 0.8,
            35: 0.7,
            37: 0.5,
            40: 0.3,
        }

        age_multiplier = 0
        for ageRequired, multiplier in age_factor_mapping.items():
            if ageRequired > age:
                break
            else:
                age_multiplier = multiplier

        club_reputation_mapping = {
            1: 0,
            55: 0.4,
            60: 0.6,
            65: 0.7,
            68: 0.8,
            72: 1.0,
            82: 1.1
        }

        clubObject = clubs[self.clubID]
        clubReputation = clubObject.getReputation()
        club_reputation_multiplier = 0
        for reputationRequired, multiplier in club_reputation_mapping.items():
            if reputationRequired > clubReputation:
                break
            else:
                club_reputation_multiplier = multiplier

        league_reputation_mapping = {
            1: 0,
            55: 0.4,
            69: 0.5,
            75: 0.8,
            82: 1.05
        }

        leagueID = clubObject.getLeague()
        leagueObject = leagues[leagueID]
        leagueReputation = leagueObject.getReputation()
        league_reputation_multiplier = 0
        for reputationRequired, multiplier in league_reputation_mapping.items():
            if reputationRequired > leagueReputation:
                break
            else:
                league_reputation_multiplier = multiplier

        league_nation_reputation_mapping = {
            1: 0,
            60: 0.6,
            65: 0.7,
            68: 0.8,
            72: 1,
            82: 1.05,
            90: 1.1,
        }

        nationID = leagueObject.getNation()
        nationObject = nations[nationID]
        nationReputation = nationObject.getReputation()
        nation_reputation_multiplier = 0
        for reputationRequired, multiplier in league_nation_reputation_mapping.items():
            if reputationRequired > nationReputation:
                break
            else:
                nation_reputation_multiplier = multiplier


        contract_length_mapping = {
            1: 0.4,
            2: 0.7,
            3: 0.9,
            4: 1.0,
            5: 1.05,
            6: 1.1
        }

        contract_length_multiplier = 0
        for contractLengthRequired, multiplier in contract_length_mapping.items():
            if contractLengthRequired > self.contract_length:
                break
            else:
                contract_length_multiplier = multiplier

        multiplier = league_reputation_multiplier * age_multiplier * nation_reputation_multiplier * club_reputation_multiplier * contract_length_multiplier


        # USING EXPONENTIAL MODELLING

        if Player.calculateRating(self) < 80:
            value = 0 # Players of this ability are most likely semi-professional
        elif Player.calculateRating(self) < 105:
            value = 0.3583 * (1.12694 ** Player.calculateRating(self)) # Lower end National League players to top end League Two
        elif Player.calculateRating(self) < 140:
            value = 295.67 * (1.08042 ** Player.calculateRating(self)) # League One to decent Premier League
        elif Player.calculateRating(self) < 190:
            value = 6407.6 * (1.05799 ** Player.calculateRating(self)) # Premier League + Elite Players
        else:
            value = 250000000 # MAX VALUE - No team will pay more than this on one player

        value = value * multiplier
        value = float(f"{value:.2g}")
        value = int(value)

        return value

    # ENSURES KEY ATTRIBUTES GROW RAPIDLY
    def high_curve(x):
        return (x / 10) ** 1.4 * 10

    # ENSURES DECENTLY IMPORTANT ATTRIBUTES GROW EXPONENTIALLY
    def mid_curve(x):
        return (x / 10) ** 1.1 * 10


    def calculateRating(self, position=None):


        if position is None:
            position = self.position.getID()

        position_weights = {
            1: self.GOALKEEPER_WEIGHTS,
            3: self.CENTREBACK_WEIGHTINGS,
            2: self.FULLBACK_WEIGHTINGS,
            4: self.FULLBACK_WEIGHTINGS,
            5: self.DEFENSIVE_MIDFIELDER_WEIGHTINGS,
            6: self.CENTRAL_MIDFIELDER_WEIGHTINGS,
            7: self.ATTACKING_MIDFIELDER_WEIGHTINGS,
            9: self.WINGER_WEIGHTINGS,
            8: self.WINGER_WEIGHTINGS,
            10: self.STRIKER_WEIGHTINGS
        }

        weight = position_weights[position]

        ability = (
                weight["passing"] * Player.mid_curve(self.passing) +
                weight["dribbling"] * Player.high_curve(self.dribbling) +
                weight["finishing"] * Player.high_curve(self.finishing) +

                weight["defending"] * Player.mid_curve(self.defending) +

                weight["ball_control"] * Player.mid_curve(self.ball_control) +
                weight["delivery"] * Player.mid_curve(self.delivery) +
                weight["vision"] * Player.mid_curve(self.vision) +

                weight["football_iq"] * Player.mid_curve(self.football_iq) +

                weight["positioning"] * Player.mid_curve(self.positioning) +
                weight["composure"] * Player.mid_curve(self.composure) +
                weight["decision_making"] * Player.mid_curve(self.decision_making) +

                weight["work_rate"] * self.work_rate +
                weight["aggression"] * self.aggression +

                weight["pace"] * Player.high_curve(self.pace) +

                weight["strength"] * Player.mid_curve(self.strength) +
                weight["stamina"] * self.stamina +
                weight["aerial"] * Player.mid_curve(self.aerial) +

                weight["shot_stopping"] * Player.high_curve(self.shot_stopping) +
                weight["handling"] * Player.mid_curve(self.handling) +
                weight["distribution"] * Player.mid_curve(self.distribution) +
                weight["command"] * Player.mid_curve(self.command)
        )

        # SCALES UP FROM MAX 20 CA TO 200
        ability = ability * 10

        if position != self.position.getID():
            ability = ability * Player.SECONDARY_POSITION_FAMILIARITY

        return int(round(ability))


    def canPlayPosition(self, position):
        primary = self.position.getID()
        if position == primary:
            return True
        else:
            alternate_positions = Player.secondary_position_mapping[primary]
            for alternatePosition in alternate_positions:
                if position == alternatePosition:
                    return True
            return False

    def getID(self):
        return self.id

    def getName(self):
        if self.firstname != "":
            return f"{self.firstname} {self.surname}"
        else:
            return f"{self.surname}"

    def getAge(self, date):
        cDay, cMonth, cYear = date.getDate()

        age = cYear - self.birthYear

        if cMonth == self.birthMonth and cDay <= self.birthDay:
            age = age - 1
        elif cMonth < self.birthMonth:
            age = age - 1

        return age

    def getBirthday(self):
        return f"{self.birthDay}/{self.birthMonth}/{self.birthYear}"

    def getNationality(self):
        return self.nationality

    def setPosition(self, positionObject):
        self.position = positionObject

    def getPosition(self):
        return self.position

    def getAttributes(self):
        return (self.passing, self.dribbling, self.finishing, self.defending, self.ball_control, self.delivery,
                self.vision, self.football_iq, self.positioning, self.composure, self.decision_making, self.work_rate, self.aggression,
                 self.pace, self.strength, self.stamina, self.aerial, self.shot_stopping, self.handling, self.distribution, self.command)

    def getContractLength(self):
        return self.contract_length

    def decrementContractLength(self):
        self.contract_length = self.contract_length - 1

    def getCurrentWage(self):
        return self.current_wage

    def getClub(self):
        return self.clubID

    def getParentClub(self):
        return self.parentClubID

    def getLoanClub(self):
        return self.loanClubID

    def setClub(self, clubID):
        if clubID is not None:
            self.clubID = int(clubID)
        else:
            self.clubID = None

    def setParentClub(self, parentClubID):
        if parentClubID is not None:
            self.parentClubID = int(parentClubID)
        else:
            self.parentClubID = None

    def setLoanClub(self, loanID):
        if loanID is not None:
            self.loanClubID = int(loanID)
        else:
            self.loanClubID = None

    def calculateStarRating(self, players):

        star_emojis = {
            1.5: "🟢🟡⚫⚫⚫",
            2.0: "🟢🟢⚫⚫⚫",
            2.5: "🟢🟢🟡⚫⚫",
            3.0: "🟢🟢🟢⚫⚫",
            3.5: "🟢🟢🟢🟡⚫",
            4.0: "🟢🟢🟢🟢⚫",
            4.5: "🟢🟢🟢🟢🟡",
            5.0: "🟢🟢🟢🟢🟢"
        }

        if type(players) == list:
            tempDict = {}
            for player in players:
                tempDict[player.getID()] = player
            players = tempDict

        # ADDS PLAYER TO PLAYERS DICT IF NOT IN ALREADY

        temp_added = False
        if self.id not in players.keys():
            temp_added = True
            players[self.id] = self

        abilities = {}
        for id, object in players.items():
            abilities[id] = object.calculateRating()

        import statistics

        average = statistics.mean(abilities.values())
        std = statistics.stdev(abilities.values()) or 1

        z = (Player.calculateRating(self) - average) / std

        stars = 3 + z
        stars = round(stars * 2) / 2
        stars = max(1.5, min(5, stars))


        returnValue = star_emojis[stars]

        if temp_added:
            del players[self.id]

        return returnValue

class freeAgents:

    COLOR_MAPPING = {
        "black": "⚫",
        "white": "⚪",
    }

    def __init__(self, id, full_name, short_name):
        self.id = id
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

    def getLeague(self):
        return None

    def getNation(self):
        return None

    def getReputation(self):
        return self.reputation

    def printColors(self):
        return f"{self.COLOR_MAPPING[self.primary_color]}{self.COLOR_MAPPING[self.secondary_color]}"

    def getFixtures(self):
        return self.fixtures

    def clearSeasonData(self):
        return

class Club:
    FORMATIONS = {
        "433": [1, 2, 3, 3, 4, 5, 6, 6, 8, 10, 9],
        "4231": [1, 2, 3, 3, 4, 5, 5, 8, 7, 9, 10],
        "442": [1, 2, 3, 3, 4, 8, 6, 6, 9, 10, 10],
        "5221": [1, 2, 3, 3, 3, 4, 5, 5, 7, 7, 10],
        "5212": [1, 2, 3, 3, 3, 4, 5, 5, 7, 10, 10]
    }

    COLOR_MAPPING = {
        "black": "⚫",
        "white": "⚪",
        "blue": "🔵",
        "red": "🔴",
        "yellow": "🟡",
        "orange": "🟠",
        "purple": "🟣",
        "green": "🟢"
    }

    def __init__(self, id, full_name, short_name, nickname, founded_date, transfer_budget, primary_color, secondary_color, reputation, league):
        self.id = int(id)
        self.full_name = full_name
        self.short_name = short_name
        self.nickname = nickname
        self.founded_date = int(founded_date)
        self.transfer_budget = int(transfer_budget)

        self.players = []
        self.first_team = []
        self.youth_team = []

        self.fixtures = []
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.reputation = int(reputation)
        self.league = int(league)
        self.manager = 0
        self.stadium = 0
        self.formation = None
        self.starting_eleven = []
        self.bench = []

        self.matchesPlayed = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.goalsFor = 0
        self.goalsAgainst = 0

    def getLeague(self):
        return self.league

    def setLeague(self, league):
        self.league = int(league)

    def getID(self):
        return self.id

    def getName(self):
        return self.full_name

    def getFullName(self):
        return self.full_name

    def getShortName(self):
        return self.short_name

    def getFoundedDate(self):
        return self.founded_date

    def getNickname(self):
        return self.nickname

    def getTransferBudget(self):
        return self.transfer_budget

    def getReputation(self):
        return self.reputation

    def getTotalPlayerWages(self):
        total_wages = 0
        for player in self.players:
            w = player.getCurrentWage()
            total_wages += w
        return int(total_wages)

    def addPlayer(self, player):
        self.players.append(player)

    def getPlayers(self):
        return self.players

    def getFirstTeam(self):
        return self.first_team

    def getYouthTeam(self):
        return self.youth_team

    def setManager(self, manager):
        self.manager = manager

    def getManager(self):
        return self.manager

    def setStadium(self, stadium):
        self.stadium = stadium

    def getStadium(self):
        return self.stadium

    def printColors(self):
        return f"{self.COLOR_MAPPING[self.primary_color]}{self.COLOR_MAPPING[self.secondary_color]}"

    def addFixture(self, fixture):
        self.fixtures.append(fixture)

    def getFixtures(self):
        return self.fixtures

    def autoPickTeam(self):
        team_sheet = {}
        starting_eleven = []
        bench = []
        MAX_SIZE_OF_BENCH = 7

        # GETS PREFERRED FORMATION FROM MANAGER
        formation = Club.FORMATIONS[self.manager.getPreferredFormation()]

        # SELECTS THE BEST PLAYER FOR EACH POSITION

        # Eventually will filter through injured players and remove them
        available_players = self.players.copy()

        for position in formation:
            best_player = None
            for player in available_players:
                # CHECKS IF THERE IS NO CURRENTLY SELECTED BEST PLAYER
                if best_player is None:
                    best_player = player
                else:
                    # Eventually will also consider fitness when considering player ratings here
                    if (player.calculateRating(position) > best_player.calculateRating(position)) and player.canPlayPosition(position) == True:
                        best_player = player
            starting_eleven.append(best_player)

            # REMOVES SELECTED PLAYER FROM AVAILABLE PLAYERS
            available_players.remove(best_player)


        # ORGANIZES REMAINING PLAYERS BASED ON ABILITY TO GET BENCH

        available_players.sort(key=lambda p: p.calculateRating(), reverse = True)

        for i in range(MAX_SIZE_OF_BENCH):
            bench.append(available_players[i])

        return formation, starting_eleven, bench

    def calculateTeamStrength(self):

        formation, starting_eleven, bench = Club.autoPickTeam(self)
        starting_eleven_total = 0
        bench_total = 0
        for index, player in enumerate(starting_eleven):
            position = formation[index]
            starting_eleven_total = (player.calculateRating(position)) + starting_eleven_total
        for index, player in enumerate(bench):
            bench_total = (player.calculateRating()) + bench_total

        bench_mean = bench_total / len(bench)

        # STARTING XI HAS MORE IMPORTANCE - ALL PLAYERS HAVE IMPACT IN XI THEREFORE USES TOTAL, NOT ALL PLAYERS ON BENCH WILL BE USED HENCE MEAN
        score = (starting_eleven_total * 0.95) + (bench_mean * 0.05)
        return round(score)


    # USED IN MEDIA PREDICTION
    def calculateBettingOdds(self, game):

        # SPLITS TEAMS FURTHER APART IN BETTING ODDS
        amplification_factor = 14

        clubs = game.getClubs()
        leagues = game.getLeagues()
        leagueID = self.league
        leagueObject = leagues[leagueID]
        clubsInLeague = leagueObject.getClubs()

        # GETTING TOTAL TEAM STRENGTH OF ALL SIDES IN LEAGUE
        total = 0
        for club in clubsInLeague:
            total = total + clubs[club].calculateTeamStrength() ** amplification_factor

        # CALCULATING RATING INTO PROBABILITY
        probability = self.calculateTeamStrength() ** amplification_factor/ total

        # CONVERTS TO FRACTIONAL ODDS
        decimal_odds = 1/probability

        fractional = decimal_odds - 1

        # ONLY ROUNDS LONG ODDS
        if fractional >= 100:
            fractional = round(fractional / 50) * 50
        elif fractional >= 20:
            fractional = round(fractional / 10) * 10
        else:
            fractional = round(fractional)

        return int(fractional)

    def autoSplitPlayers(self, date):

        if len(self.first_team) != 0:
            self.first_team = []
        if len(self.youth_team) != 0:
            self.youth_team = []

        for player in self.players:
            if player.getAge(date) > 22:
                self.first_team.append(player)
            else:
                self.youth_team.append(player)

        # Checks if any players need to be demoted from first team to youth setup

        total = 0
        for player in self.first_team:
            total = total + player.calculateRating()

        mean = total/len(self.first_team)

        demoted = []
        for player in self.first_team:
            change = player.calculateRating() / mean
            if change < 0.8:
                demoted.append(player)

        for player in demoted:
            self.first_team.remove(player)
            self.youth_team.append(player)

        # Goes through youth squad and checks if any players are first-team ready by comparing their CA with the player with the least ability under 30 in first team

        self.first_team.sort(key=lambda p: p.calculateRating())
        for player in self.first_team:
            if player.getAge(date) < 30:
                minPlayer = player
                break

        promoted = []

        for player in self.youth_team:
            if minPlayer.calculateRating() - player.calculateRating() < 4:
                promoted.append(player)

        for player in promoted:
            self.youth_team.remove(player)
            self.first_team.append(player)





    def getTeamSheet(self):
        return self.formation, self.starting_eleven, self.bench

    def setTeamSheet(self, formation, starting_eleven, bench):
        self.formation = formation
        self.starting_eleven = starting_eleven
        self.bench = bench

    def getMatchesPlayed(self):
        return self.matchesPlayed
    def incrementMatchesPlayed(self):
        self.matchesPlayed += 1
    def getWins(self):
        return self.wins
    def incrementWins(self):
        self.wins += 1
    def getLosses(self):
        return self.losses
    def incrementLosses(self):
        self.losses += 1
    def getDraws(self):
        return self.draws
    def incrementDraws(self):
        self.draws += 1
    def getGoalsFor(self):
        return self.goalsFor
    def incrementGoalsFor(self):
        self.goalsFor += 1
    def getGoalsAgainst(self):
        return self.goalsAgainst
    def incrementGoalsAgainst(self):
        self.goalsAgainst += 1
    def getGoalDifference(self):
        return self.goalsFor - self.goalsAgainst
    def getPoints(self):
        points = (self.wins * 3) + self.draws
        return points
    def clearSeasonData(self):
        self.matchesPlayed = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goalsFor = 0
        self.goalsAgainst = 0


class Position:
    def __init__(self, id, abbreviation, name):
        self.id = int(id)
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