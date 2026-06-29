from read_from_file import *
from classes import *
from cli import *
from random import randint

def read_from_file_function():
    players = read_players_from_file()
    positions = read_positions_from_file()
    clubs = read_clubs_from_file()
    leagues = read_leagues_from_file()
    managers = read_managers_from_file()
    stadiums = read_stadiums_from_file()
    nations = read_nations_from_file()
    loans = read_loans_from_file()
    return players,positions,clubs,leagues,managers,stadiums,nations,loans


def game_initialisation(players, positions, clubs, leagues, managers, stadiums, nations, loans):

    # CREATES DATE OBJECT
    date = Date()

    # CREATES FREE AGENT OBJECT

    f = freeAgents(0, "Free Agents", "Free Agents")
    clubs[f.getID()] = f

    # LOADS DATA FROM FILES AND ASSIGNS EVERYTHING TO EACH OTHER

    initialize_loans(players, loans)
    initialize_players(players,clubs)
    initialize_leagues(clubs,leagues)
    initialize_managers(managers,clubs)
    initialize_stadiums(stadiums,clubs)
    initialize_positions(players,positions)
    #initialize_nations(nations, players, managers)

    # INSTANTIATES GAME CLASS
    game = gameObject(date, players, positions, clubs, leagues, managers, stadiums, nations)

    date.setDate(2, 7, 2025)

    for league in leagues.values():
        tempDate = copy.deepcopy(game.getDateObject())
        league.arrangeFixtures(tempDate)

    return game



def match_sim_test(game, fixture):

    homeScore = randint(1, 4)
    awayScore = randint(1, 4)

    # POST MATCH PROCESSING
    fixture.setScore(homeScore, awayScore)
    homeClub, awayClub = fixture.getTeams()
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


def match_checker(game):
    dateObject = game.getDateObject()

    # CHECKS FOR MATCHES

    leagues = game.getLeagues()
    for league in leagues.values():
        fixtures = league.getFixtures()
        for fixture in fixtures:
            if fixture.getDate() == dateObject.getDate():
                match_sim_test(game, fixture)



def game_loop(game):

    while True:
        dateObject = game.getDateObject()

        day, month, year = dateObject.getDate()

        if (day == 25) and (month == 6):
            game.seasonUpdate()

        if (day == 1) and (month == 7):
            game.annualUpdate()


        # RUNS MENU IF NOT AUTO-SIMULATING
        if game.getHolidayStatus() is not True:
            value = game_main_menu(game)
            if value == "Return to main menu":
                break
            elif value == "Advance":
                match_checker(game)
                dateObject.advance()

        # ADVANCES DAYS AUTOMATICALLY WHEN 'HOLIDAYING'
        else:
            match_checker(game)
            dateObject.advance()
            if game.getHolidayDate() == dateObject.getDate():
                game.endHoliday()

    initial_menu()


def createManager(managers):
    clubs = read_clubs_from_file()
    nations = read_nations_from_file()

    firstName = None
    lastName = None
    age = None
    nation = None
    club = None
    while True:
        ui = option_menu(["First Name", "Last Name", "Age", "Nationality", "Club", "Continue"], False, "🧑‍💼 Let's create your manager - fill out all fields:")
        if ui == 1:
            firstName = user_input("string", "Enter your first name: ")
            print(f"✅ First Name set to '{firstName}'!")
        elif ui == 2:
            lastName = user_input("string", "Enter your first name: ")
            print(f"✅ Last Name set to '{lastName}'!")
        elif ui == 3:
            passed = False
            while not passed:
                age = user_input("integer", "Enter your age: ")
                if 0 < age <= 200:
                    passed = True
                else:
                    print("🚫 Invalid age!")
            print(f"✅ Age set to {age}!")
        elif ui == 4:
            nationID, nation = search(nations)
            print(f"✅ Nationality set to {nation.getName()}!")
        elif ui == 5:
            clubID, club = search(clubs)
            print(f"✅ Selected {club.getName()}!")
            print()
        elif ui == 6:
            if firstName is not None and lastName is not None and age is not None and club is not None and nation is not None:
                break
            else:
                print("🚫 All fields must be completed!")

    ID = len(managers) + 1
    playerManager = PlayerManager(ID, firstName, lastName, age, nationID, clubID)

    for manager in managers.values():
        if manager.getClub() == clubID:
            manager.setClub(0)
            playerManager.setClub(clubID)

    managers[int(playerManager.getID())] = playerManager

    return managers

# USED FOR TESTING PURPOSES TO BYPASS INITIAL MANAGER CREATION SCREEN IMMEDIATELY
def autoCreateManager(managers):
    ID = len(managers) + 1
    firstName = "Cole"
    lastName = "Jervis"
    age = 20
    nationID = 1
    clubID = randint(1,20)
    playerManager = PlayerManager(ID, firstName, lastName, age, nationID, clubID)

    for manager in managers.values():
        if manager.getClub() == clubID:
            manager.setClub(0)
            playerManager.setClub(clubID)

    managers[int(playerManager.getID())] = playerManager

    return managers


def initial_menu():
    print("")

    while True:
        ui = (option_menu(["Start a new game", "Close Game", "Test"]))
        if ui == 1:
            players, positions, clubs, leagues, managers, stadiums, nations, loans = read_from_file_function()
            managers = createManager(managers)
            game = game_initialisation(players, positions, clubs, leagues, managers, stadiums, nations, loans)
            game_loop(game)
        elif ui == 2:
            break
        elif ui == 3:
            players, positions, clubs, leagues, managers, stadiums, nations, loans = read_from_file_function()
            managers = autoCreateManager(managers)
            game = game_initialisation(players, positions, clubs, leagues,managers, stadiums, nations, loans)
            game_loop(game)
        break
