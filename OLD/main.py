import random

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
        return f"{self.day}/{self.month}/{self.year}"

    def isLeapYear(self):
        return (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0)

    def days_in_february(self):
        if self.month == 2:
            if self.isLeapYear() == True:
                return 29
            else:
                return 28

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


class Person:
    def __init__(self, id, firstname, surname, age, nationality):
        self.id = id
        self.firstname = firstname
        self.surname = surname
        self.age = age
        self.nationality = nationality


class Stadium:
    def __init__(self, id, name, clubID, capacity):
        self.id = id
        self.name = name
        self.clubID = clubID
        self.capacity = capacity

    def getClub(self):
        return self.clubID

    def getName(self):
        return self.name

    def getCapacity(self):
        return self.capacity


class Manager(Person):
    def __init__(self, id, firstname, surname, age, nationality, clubID, preferred_formation):
        Person.__init__(self, id, firstname, surname, age, nationality)
        self.clubID = clubID
        self.preferred_formation = preferred_formation

    def getPreferredFormation(self):
        return self.preferred_formation

    def getName(self):
        return self.firstname + " " + self.surname

    def getClub(self):
        return self.clubID


class League:
    def __init__(self, id, name, reputation, start_date):
        self.id = id
        self.name = name
        self.reputation = int(reputation)
        self.clubs = {}
        self.fixtures = []
        self.start_date = start_date

    def getName(self):
        return self.name

    def addClub(self, id, club):
        self.clubs[id] = club

    def getClubs(self):
        return self.clubs

    def getFixtures(self):
        return self.fixtures

    def arrangeFixtures(self, DateObject):

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
                        f = Fixture(id, club, secondClub)
                        fixtures.append(f)

        print(len(fixtures))
        amount_of_fixtures = len(fixtures)

        # SPLITS INTO SEPARATE MATCH DAYS AND FINDS AVAILABLE DAY, while loop needed as in some cases, algorithm breaks when not shuffled correctly

        matchdays_count = 2 * (len(self.clubs) - 1)
        print(matchdays_count)

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


        for fixture in self.fixtures:
            home, away = fixture.getTeams()
            print(f"{home.getName()} {away.getName()} {fixture.getDate()}")
        print(len(self.fixtures))


class Fixture:
    def __init__(self, id, homeClub, awayClub, date=None):
        self.id = id
        self.homeClub = homeClub
        self.awayClub = awayClub
        self.date = date

    def getTeams(self):
        return self.homeClub, self.awayClub

    def setDate(self, date):
        self.date = date

    def getDate(self):
        return self.date


class Player(Person):
    GOALKEEPER_WEIGHTS = {
        "reflexes": 0.30,
        "handling": 0.30,
        "positioning": 0.20,
        "passing": 0.10,
        "physical": 0.10
    }

    CENTREBACK_WEIGHTINGS = {
        "pace": 0.10,
        "shooting": 0.00,
        "passing": 0.05,
        "dribbling": 0.05,
        "defending": 0.45,
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
        "pace": 0.10,
        "shooting": 0.25,
        "passing": 0.30,
        "dribbling": 0.25,
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
        "pace": 0.25,
        "shooting": 0.40,
        "passing": 0.05,
        "dribbling": 0.15,
        "defending": 0.00,
        "physical": 0.15
    }

    SECONDARY_POSITION_FAMILIARITY = 0.9

    secondary_position_mapping = {
        "CB": ["LB", "RB"],
        "CM": ["CDM", "CAM"],
        "CDM": ["CM"],
        "CAM": ["CM"],
        "LW": ["RW"],
        "RW": ["LW"]
    }

    def __init__(self, id, firstname, surname, age, nationality, clubID, position, pace, shooting, passing, dribbling,
                 defending, physical, reflexes, handling, positioning, potential, current_wage, contract_length):
        super().__init__(id, firstname, surname, age, nationality)
        self.clubID = clubID
        self.position = position
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

    def calculateRating(self, position=None):

        if position is None:
            position = self.position

        position_weights = {
            "GK": self.GOALKEEPER_WEIGHTS,
            "CB": self.CENTREBACK_WEIGHTINGS,
            "RB": self.FULLBACK_WEIGHTINGS,
            "LB": self.FULLBACK_WEIGHTINGS,
            "CDM": self.DEFENSIVE_MIDFIELDER_WEIGHTINGS,
            "CM": self.CENTRAL_MIDFIELDER_WEIGHTINGS,
            "CAM": self.ATTACKING_MIDFIELDER_WEIGHTINGS,
            "LW": self.WINGER_WEIGHTINGS,
            "RW": self.WINGER_WEIGHTINGS,
            "ST": self.STRIKER_WEIGHTINGS
        }

        weight = position_weights[position]

        if position == "GK":
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

        if position != self.position:
            ability = ability * Player.SECONDARY_POSITION_FAMILIARITY

        return int(round(ability))

    def getName(self):
        return f"{self.firstname} {self.surname}"

    def getPosition(self):
        return self.position

    def getAttributes(self):
        if self.position == "GK":
            return self.reflexes, self.handling, self.positioning
        else:
            return self.pace, self.shooting, self.passing, self.dribbling, self.defending, self.physical

    def getClub(self):
        return self.clubID

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

        abilities = {}
        for id, object in players.items():
            abilities[id] = object.calculateRating()

        star_ratings = {}
        min_ca = min(abilities.values())
        max_ca = max(abilities.values())

        for id, ca in abilities.items():
            if max_ca == min_ca:
                relative = 1
            else:
                relative = (ca - min_ca) / (max_ca - min_ca)
                stars = 1.5 + relative * 3.5
                stars = round(stars * 2) / 2
                star_ratings[id] = stars

        return star_emojis[star_ratings[self.id]]


class Club:
    FORMATIONS = {
        "433": ["GK", "RB", "CB", "CB", "LB", "CDM", "CM", "CM", "RW", "ST", "LW"],
        "4231": ["GK", "RB", "CB", "CB", "LB", "CDM", "CDM", "RW", "CAM", "LW", "ST"],
        "442": ["GK", "RB", "CB", "CB", "LB", "RW", "CM", "CM", "LW", "ST", "ST"],
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

    def __init__(self, id, name, transfer_budget, primary_color, secondary_color, reputation, league):
        self.id = id
        self.name = name
        self.transfer_budget = int(transfer_budget)
        self.players = {}
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.reputation = int(reputation)
        self.league = league
        self.manager = 0

    def getName(self):
        return self.name

    def addPlayer(self, id, player):
        self.players[id] = player

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

    def getLeague(self):
        return self.league

    def autoPickTeam(self):
        team_sheet = {}
        MAX_SIZE_OF_BENCH = 7

        positions = {
            "GK": [],
            "RB": [],
            "CB": [],
            "LB": [],
            "CDM": [],
            "CM": [],
            "CAM": [],
            "RW": [],
            "LW": [],
            "ST": []
        }

        # POPULATES EACH LIST FOR EACH POSITION'S PLAYERS IN ABOVE POSITIONS DICTIONARY
        for player in self.players.values():
            positions[player.getPosition()].append(player)
            for primaryPosition, alternativePositionsList in Player.secondary_position_mapping.items():
                if primaryPosition == player.getPosition():
                    for alternativePosition in alternativePositionsList:
                        positions[alternativePosition].append(player)

        # SORTING PLAYERS BY RATING
        for pos in positions:
            positions[pos].sort(key=lambda player: player.calculateRating(pos), reverse=True)

        # GETS FORMATION FROM MANAGER, AND ASSIGNS FORMATION TO STARTING XI
        self.formation = self.manager.getPreferredFormation()
        startingXI = self.FORMATIONS[self.formation].copy()

        # ADDS PLAYER TO STARTING XI AND REMOVES ALL INSTANCES OF THE PLAYER FROM POSITIONS LISTS
        for index, position in enumerate(startingXI):
            selected_player = positions[position][0]
            startingXI[index] = selected_player

            # Remove this player from ALL position lists
            for pos_list in positions.values():
                if selected_player in pos_list:
                    pos_list.remove(selected_player)

        # POPULATE BENCH
        bench = []
        remaining_players = []
        for position, list in positions.items():
            for index, player in enumerate(list):
                remaining_players.append(player)

                # Removes duplicates
                for pos_list in positions.values():
                    if player in pos_list:
                        pos_list.remove(player)

        # SORTING PLAYERS BY RATING
        remaining_players.sort(key=lambda player: player.calculateRating(), reverse=True)

        for i in range(MAX_SIZE_OF_BENCH):
            bench.append(remaining_players[i])

        return startingXI, bench


def initialize_stadiums(stadiums, clubs):
    for id, stadium in stadiums.items():
        club = stadium.getClub()
        if club in clubs:
            clubs[club].setStadium(stadium)


def initialize_managers(managers, clubs):
    for id, manager in managers.items():
        club = manager.getClub()
        if club in clubs:
            clubs[club].setManager(manager)


def initialize_players(players, clubs):
    for id, player in players.items():
        club = player.getClub()
        if club in clubs:
            clubs[club].addPlayer(id, player)


def initialize_leagues(clubs, leagues):
    for id, club in clubs.items():
        league = club.getLeague()
        if league in leagues:
            leagues[league].addClub(id, club)


def read_players_from_file():
    players = {}
    with open("players.fmdata") as file:
        for line_number, line in enumerate(file, start=1):
            data = line.strip().split("-")

            # USED TO ENSURE CODE DOESN'T BREAK IF A PLAYER HAS AN BAD ENTRY
            if len(data) != 19:
                print(f"Line {line_number} has {len(data)} parts: {data}")
                continue

            p = Player(*data)
            players[data[0]] = p

        return players


def read_clubs_from_file():
    clubs = {}
    with open("clubs.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Club(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            clubs[data[0]] = c
    return clubs


def read_managers_from_file():
    managers = {}
    with open("managers.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Manager(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            managers[data[0]] = c
    return managers


def read_stadiums_from_file():
    stadiums = {}
    with open("stadiums.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Stadium(data[0], data[1], data[2], data[3])
            stadiums[data[0]] = c
    return stadiums


def read_leagues_from_file():
    leagues = {}
    with open("leagues.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = League(data[0], data[1], data[2], data[3])
            leagues[data[0]] = c
    return leagues


def search(data):
    while True:
        SearchEntries = {}
        userInput = input("Search name: ")
        print("")

        for id, item in data.items():
            if userInput.lower() in item.getName().lower():
                SearchEntries[id] = item

        if len(SearchEntries) == 0:
            print("❌ Found no results for '" + userInput + "'!")
        elif len(SearchEntries) == 1:
            for id, item in SearchEntries.items():
                return id, item
        else:
            print(f"Found {len(SearchEntries)} search results:")
            SearchEntriesList = []
            for id, item in SearchEntries.items():
                SearchEntriesList.append(id)
            for position, id in enumerate(SearchEntriesList, start=1):
                print(f"{position} - {SearchEntries[id].getName()}")
            passed = False
            while not passed:
                userInput = input("Please select the number corresponding to which item you want to select: ")
                try:
                    userInput = int(userInput) - 1
                    passed = True
                except ValueError:
                    print("Please enter a number.")

            selectedItem = SearchEntriesList[userInput]
            return selectedItem, SearchEntries[selectedItem]


def seasonUpdate(players, clubs, leagues, managers, stadiums, DateObject):
    for league in leagues.values():
        league.arrangeFixtures(DateObject)


def game():
    # ALL NECESSARY WHEN STARTING A NEW GAME
    DateObject = Date()

    clubs = read_clubs_from_file()
    players = read_players_from_file()
    managers = read_managers_from_file()
    stadiums = read_stadiums_from_file()
    leagues = read_leagues_from_file()
    initialize_players(players, clubs)
    initialize_managers(managers, clubs)
    initialize_stadiums(stadiums, clubs)
    initialize_leagues(clubs, leagues)

    seasonUpdate(players, clubs, leagues, managers, stadiums, DateObject)
    DateObject.setDate(1, 7, 2025)
    while True:
        print(f"{DateObject.getDate()} | {DateObject.getWeekday()}")
        userInput = input("")
        if userInput == "":
            DateObject.advance()
        if userInput == "1":
            id, league = search(leagues)
            fixtures = league.getFixtures()
            for fixture in fixtures.values():
                home, away = fixture.getTeams()
                print(home.getName(), away.getName())


game()





