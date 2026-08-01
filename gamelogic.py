from read_from_file import *
from classes import *
from cli import *
from random import randint
from classes import *
from read_from_file import *
from match_engine import simulate_match
from match_engine import simulate_match_extra_time
from match_engine import simulate_penalties

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

    # ARRANGES ALL LEAGUE'S FIXTURES
    for league in leagues.values():
        tempDate = copy.deepcopy(game.getDateObject())
        league.arrangeFixtures(tempDate)

    # SPLITS CLUB PLAYERS INTO FIRST TEAM AND YOUTH ACADEMY

    for club in clubs.values():
        if club.getID() != 0:
            club.autoSplitPlayers(date)

    return game



def match_sim_processing(game, fixture):
    homeTeam, awayTeam = fixture.getTeams()

    tournamentID = fixture.getLeagueID()
    if tournamentID is None:
        tournamentID = fixture.getTournamentID()

    # REGISTERS ALL PLAYERS FOR TOURNAMENT

    for player in homeTeam.getPlayers():
        if tournamentID not in player.seasonData.keys():
            player.addTournamentToSeasonData(tournamentID)
    for player in awayTeam.getPlayers():
        if tournamentID not in player.seasonData.keys():
            player.addTournamentToSeasonData(tournamentID)

    simulate_match(fixture, game)

    # REMOVING RED CARDS
    for player in homeTeam.getPlayers():
        player.isSentOff = False
    for player in awayTeam.getPlayers():
        player.isSentOff = False

    if fixture.getType() == "league":
        leagues = game.getLeagues()
        leagueID = fixture.getLeagueID()
        leagueObject = leagues[leagueID]
        leagueObject.postMatchProcessing(fixture)


    elif fixture.getType() == "knockout":

        if fixture.getLeg() is None:
            homeScore, awayScore = fixture.getScore()
            if homeScore == awayScore:
                simulate_match_extra_time(fixture, game)
                homeScore, awayScore = fixture.getScore()
            if homeScore == awayScore:
                simulate_penalties(fixture)


        if fixture.getLeg() == 2:
            homeScore, awayScore = fixture.getScore()
            firstLeg = fixture.getPartnerFixture()
            firstLegHomeScore, firstLegAwayScore = firstLeg.getScore()  # leg1: TeamA home, TeamB away

            # leg2 home = TeamB, away = TeamA - VENUE HAS BEEN SWAPPED
            aggHome = firstLegAwayScore + homeScore  # TeamB's aggregate
            aggAway = firstLegHomeScore + awayScore  # TeamA's aggregate

            if aggHome == aggAway:
                simulate_match_extra_time(fixture, game)
                homeScore, awayScore = fixture.getScore()
                aggHome = firstLegAwayScore + homeScore  # TeamB's aggregate
                aggAway = firstLegHomeScore + awayScore  # TeamA's aggregate

            if aggHome == aggAway:
                simulate_penalties(fixture)

        if fixture.getLeagueID() is not None:
            leagues = game.getLeagues()
            leagueObject = leagues[fixture.getLeagueID()]
            leagueObject.postMatchProcessing(fixture)

        elif fixture.getTournamentID() is not None:
            print("") # TO BE ADDED WHEN FA CUP IS ADDED

    # ADDS PLAYER DATA TO PLAYER

    events = fixture.getMatchEvents()
    for event in events:
        if event["type"] == "chance":
            if event["outcome"] == "goal":
                player = event["scorer"]
                player.seasonData[tournamentID].goals += 1

                if event["assister"] is not None:
                    event["assister"].seasonData[tournamentID].assists += 1

        elif event["type"] == "foul":
            player = event["player"]
            if event["outcome"] == "red":
                player.seasonData[tournamentID].redCards += 1
            elif event["outcome"] == "yellow":
                player.seasonData[tournamentID].yellowCards += 1

        elif event["type"] == "substitution":
            player = event["joining-match"]
            player.seasonData[tournamentID].subAppearances += 1

    homeScore, awayScore = fixture.getScore()

    formation, starting_eleven, bench, playingStyle = homeTeam.getTeamSheet()
    homeGoalkeeper = starting_eleven[0]
    if awayScore == 0:
        homeGoalkeeper.seasonData[tournamentID].cleanSheets += 1

    formation, starting_eleven, bench, playingStyle = awayTeam.getTeamSheet()
    awayGoalkeeper = starting_eleven[0]
    if homeScore == 0:
        awayGoalkeeper.seasonData[tournamentID].cleanSheets += 1

def match_checker(game):
    dateObject = game.getDateObject()
    clubs = game.getClubs()

    processed = set()

    for club in clubs.values():
        for fixture in club.getFixtures():

            if id(fixture) in processed:
                continue

            if fixture.getDate() == dateObject.getDate():
                match_sim_processing(game, fixture)

            processed.add(id(fixture))



def game_loop(game):

    while True:
        dateObject = game.getDateObject()

        day, month, year = dateObject.getDate()

        game.morningDailyUpdate()

        if (day == 25) and (month == 6):
            game.seasonUpdate()

        if (day == 1) and (month == 7):
            game.annualUpdate()


        # RUNS MENU IF NOT AUTO-SIMULATING
        if game.getHolidayStatus() is not True:

            # CHECKS IF USER'S TEAM HAD PLAYED THE DAY BEFORE, before running main menu
            dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()
            playerManagerID = len(managers)
            playerManagerClubID = clubs[managers[playerManagerID].getClub()].getID()
            clubObject = clubs[playerManagerClubID]
            if dateObject.getYesterdayDate() is not None:
                yDay, yMonth, yYear = dateObject.getYesterdayDate()
                for fixture in clubObject.getFixtures():
                    if fixture.getDate() == (yDay, yMonth, yYear):
                        view_fixture_menu(fixture, game)


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
    clubID = randint(1,44)
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
