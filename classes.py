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

        self.onHoliday = False
        self.holidayDate = None

    def getAll(self):
        return self.dateObject, self.players, self.positions, self.clubs, self.leagues, self.managers, self.stadiums, self.nations


    def annualUpdate(self):
        for player in self.players.values():
            # INCREMENTING PLAYER AGES BY 1
            player.incrementAge()

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

    def seasonUpdate(self):

        # PROMOTION / RELEGATION LOGIC HERE

        # REMOVES ALL LEAGUE TABLE DATA FROM CLUBS
        for club in self.clubs.values():
            club.clearSeasonData()

        # FIXTURE ARRANGEMENT

        for league in self.leagues.values():
            league.getFixtures().clear()

        for club in self.clubs.values():
            club.getFixtures().clear()

        for league in self.leagues.values():
            tempDate = copy.deepcopy(self.dateObject)
            league.arrangeFixtures(tempDate)

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
    def __init__(self, id, nationID, name, reputation, start_date):
        self.id = int(id)
        self.nationID = int(nationID)
        self.name = name
        self.reputation = int(reputation)
        self.clubs = {}
        self.fixtures = []
        self.start_date = start_date

    def getLeagueID(self):
        return self.id

    def getNation(self):
        return self.nationID

    def getName(self):
        return self.name

    def addClub(self, id, club):
        self.clubs[id] = club

    def getClubs(self):
        return self.clubs

    def getFixtures(self):
        return self.fixtures

    def getReputation(self):
        return self.reputation

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
            year = DateObject.getYear()

            DateObject.setDate(day, month, year)
            while DateObject.getWeekday() != "Saturday":
                DateObject.advance()
            match_date = DateObject.getDate()

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
                        f = Fixture(id, club, secondClub, self.id)
                        fixtures.append(f)

        amount_of_fixtures = len(fixtures)

        # SPLITS INTO SEPARATE MATCH DAYS AND FINDS AVAILABLE DAY, while loop needed as in some cases, algorithm breaks when not shuffled correctly

        matchdays_count = 2 * (len(self.clubs) - 1)

        while len(self.fixtures) < amount_of_fixtures:

            random.shuffle(fixtures)
            for i in range(matchdays_count):

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

                for i in range(7):
                    DateObject.advance()
                    match_date = DateObject.getDate()
                for index, fixture in enumerate(matchday):
                    fixture.setDate(match_date)

                for fixture in matchday:
                    self.fixtures.append(fixture)

        # ADDS FIXTURES TO CLUB'S FIXTURE LIST
        for fixture in self.fixtures:
            home, away = fixture.getTeams()
            home.addFixture(fixture)
            away.addFixture(fixture)



class Fixture:
    def __init__(self, id, homeClub, awayClub, leagueID, date=None, score=None):
        self.id = int(id)
        self.homeClub = homeClub
        self.awayClub = awayClub
        self.date = date
        self.leagueID = int(leagueID)
        self.homeScore = score
        self.awayScore = score

    def getTeams(self):
        return self.homeClub, self.awayClub

    def setDate(self, date):
        self.date = date

    def getDate(self):
        return self.date

    def getLeagueID(self):
        return self.leagueID

    def getScore(self):
        if self.homeScore is None and self.awayScore is None:
            return None
        else:
            return self.homeScore, self.awayScore


    def setScore(self, homeScore, awayScore):
        self.homeScore = int(homeScore)
        self.awayScore = int(awayScore)


class Player(Person):
    GOALKEEPER_WEIGHTS = {
        "reflexes": 0.30,
        "handling": 0.30,
        "positioning": 0.20,
        "passing": 0.10,
        "physical": 0.10
    }

    CENTREBACK_WEIGHTINGS = {
        "pace": 0.15,
        "shooting": 0.00,
        "passing": 0.05,
        "dribbling": 0.05,
        "defending": 0.40,
        "physical": 0.35
    }

    FULLBACK_WEIGHTINGS = {
        "pace": 0.25,
        "shooting": 0.05,
        "passing": 0.20,
        "dribbling": 0.15,
        "defending": 0.25,
        "physical": 0.10
    }

    DEFENSIVE_MIDFIELDER_WEIGHTINGS = {
        "pace": 0.10,
        "shooting": 0.05,
        "passing": 0.30,
        "dribbling": 0.10,
        "defending": 0.30,
        "physical": 0.15
    }

    CENTRAL_MIDFIELDER_WEIGHTINGS = {
        "pace": 0.15,
        "shooting": 0.15,
        "passing": 0.30,
        "dribbling": 0.15,
        "defending": 0.15,
        "physical": 0.10
    }

    ATTACKING_MIDFIELDER_WEIGHTINGS = {
        "pace": 0.15,
        "shooting": 0.10,
        "passing": 0.35,
        "dribbling": 0.30,
        "defending": 0.05,
        "physical": 0.05
    }

    WINGER_WEIGHTINGS = {
        "pace": 0.30,
        "shooting": 0.20,
        "passing": 0.15,
        "dribbling": 0.30,
        "defending": 0.00,
        "physical": 0.05
    }

    STRIKER_WEIGHTINGS = {
        "pace": 0.20,
        "shooting": 0.40,
        "passing": 0.10,
        "dribbling": 0.15,
        "defending": 0.00,
        "physical": 0.15
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

    def __init__(self, id, firstname, surname, age, nationality, clubID, position, pace, shooting, passing, dribbling,
                 defending, physical, reflexes, handling, positioning, potential, current_wage, contract_length):
        super().__init__(id, firstname, surname, age, nationality)
        self.id = int(id)
        self.clubID = int(clubID)
        self.parentClubID = int(clubID)
        self.loanClubID = None
        self.position = int(position)
        self.pace = int(pace)
        self.shooting = int(shooting)
        self.passing = int(passing)
        self.dribbling = int(dribbling)
        self.defending = int(defending)
        self.physical = int(physical)
        self.reflexes = int(reflexes)
        self.handling = int(handling)
        self.positioning = int(positioning)
        self.potential = int(potential)
        self.current_wage = int(current_wage)
        self.contract_length = int(contract_length)

    def calculateMarketValue(self, game):

        clubs = game.getClubs()
        leagues = game.getLeagues()
        nations = game.getNations()

        # SETS MARKET VALUE TO 0 IF PLAYER IS FREE AGENT
        if self.clubID == 0:
            return 0

        age_factor_mapping = {
            1: 1.3,
            21: 1.2,
            25: 1.1,
            28: 1.0,
            31: 0.9,
            33: 0.8,
            35: 0.7,
            37: 0.5,
            40: 0.3,
        }

        age_multiplier = 0
        for ageRequired, multiplier in age_factor_mapping.items():
            if ageRequired > self.age:
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
            82: 1.2
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
            82: 1.1
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
            82: 1.2,
            90: 1.3,
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


        # USING EXPONENTIAL MODELLING - USES TWO SEPARATE EQUATIONS FOR MORE ACCURATE RESULT
        if Player.calculateRating(self) > 64:
            value = 0.085 * (1.271**Player.calculateRating(self))
        elif Player.calculateRating(self) < 65:
            value = 0.15 * (1.26**Player.calculateRating(self))

        value = value * multiplier
        value = float(f"{value:.2g}")
        value = int(value)

        return value

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

        if position == 1:
            ability = (
                    weight["reflexes"] * self.reflexes +
                    weight["handling"] * self.handling +
                    weight["positioning"] * self.positioning +
                    weight["passing"] * self.passing +
                    weight["physical"] * self.physical)
        else:
            ability = (
                    weight["pace"] * self.pace +
                    weight["shooting"] * self.shooting +
                    weight["passing"] * self.passing +
                    weight["dribbling"] * self.dribbling +
                    weight["defending"] * self.defending +
                    weight["physical"] * self.physical)

        if position != self.position.getID():
            ability = ability * Player.SECONDARY_POSITION_FAMILIARITY

        return int(round(ability))

    def getAmplificationFactor(self):
        # NEEDED - SPACES OUT PLAYER RATINGS, PARTICULARLY IN TOP LEAGUES WHERE EACH RATING INCREASE BECOMES INCREASINGLY SIGNIFICANT
        amplification_factor_mapping = {
            0: 1.00,
            65: 1.05,
            70: 1.10,
            75: 1.15,
            80: 1.20,
            83: 1.30,
            86: 1.40,
            89: 1.60
        }

        amplification_factor = 1
        for ratingRequired, multiplier in amplification_factor_mapping.items():
            if ratingRequired > self.calculateRating():
                break
            else:
                amplification_factor = multiplier

        return amplification_factor

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
        return f"{self.firstname} {self.surname}"

    def setPosition(self, positionObject):
        self.position = positionObject

    def getPosition(self):
        return self.position

    def getAttributes(self):
        return self.pace, self.shooting, self.passing, self.dribbling, self.defending, self.physical, self.reflexes, self.handling, self.positioning

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

        abilities = {}
        for id, object in players.items():
            abilities[id] = object.calculateRating()

        star_ratings = {}
        min_ca = min(abilities.values())
        max_ca = max(abilities.values())

        for id, ca in abilities.items():
            if max_ca == min_ca:
                star_ratings[id] = 3
            else:
                relative = (ca - min_ca) / (max_ca - min_ca)
                stars = 1.5 + relative * 3.5
                stars = round(stars * 2) / 2
                star_ratings[id] = stars

        return star_emojis[star_ratings[self.id]]

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

    def addManager(self, manager):
        self.managers.append(manager)

    def getManagers(self):
        return self.managers

    def getLeague(self):
        return 0

    def getNation(self):
        return 0

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
        "purple": "🟣"
    }

    def __init__(self, id, full_name, short_name, nickname, founded_date, transfer_budget, primary_color, secondary_color, reputation, league):
        self.id = int(id)
        self.full_name = full_name
        self.short_name = short_name
        self.nickname = nickname
        self.founded_date = int(founded_date)
        self.transfer_budget = int(transfer_budget)
        self.players = []
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
            amplification_factor = player.getAmplificationFactor()
            position = formation[index]
            starting_eleven_total = (player.calculateRating(position) ** amplification_factor) + starting_eleven_total
        for index, player in enumerate(bench):
            amplification_factor = player.getAmplificationFactor()
            bench_total = (player.calculateRating() ** amplification_factor) + bench_total

        bench_mean = bench_total / len(bench)

        # STARTING XI HAS MORE IMPORTANCE - ALL PLAYERS HAVE IMPACT IN XI THEREFORE USES TOTAL, NOT ALL PLAYERS ON BENCH WILL BE USED HENCE MEAN
        score = (starting_eleven_total * 0.95) + (bench_mean * 0.05)
        return round(score)


    # USED IN MEDIA PREDICTION
    def calculateBettingOdds(self, game):

        # SPLITS TEAMS FURTHER APART IN BETTING ODDS
        amplification_factor = 5

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