

def seperator():
    return "─═─" * 20

def search(data):
    while True:
        SearchEntries = {}
        userInput = input("🔍 Please enter search term: ")
        print("")

        for id, item in data.items():
            if userInput.lower() in item.getName().lower():
                SearchEntries[id] = item

        if len(SearchEntries) == 0:
            print("❌ Found no results for '" + userInput + "'!")
        elif len(SearchEntries) == 1:
            for id, item in SearchEntries.items():
                return id, item
        elif len(SearchEntries) > 10:
            print("⚠️ The search term '" + userInput + "' is too broad. Please refine your search and try again.")
        else:
            print(f"Found {len(SearchEntries)} search results:")
            SearchEntriesList = []
            for id, item in SearchEntries.items():
                SearchEntriesList.append(id)
            for position, id in enumerate(SearchEntriesList, start=1):
                print(f"{position} - {SearchEntries[id].getName()}")
            passed = False
            while not passed:
                userInput = input("🔢 Please select the number corresponding to which item you want to select: ")
                try:
                    userInput = int(userInput) - 1
                    passed = True
                except ValueError:
                    print("🔢 Please enter a number.")

            selectedItem = SearchEntriesList[userInput]
            return selectedItem, SearchEntries[selectedItem]

def option_menu(options, go_back_allowed = False, customText = False):

    number_emoji_mapping = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "1️⃣0️⃣"
    }

    options = options.copy()

    if go_back_allowed:
        options.append("Go Back")

    print(seperator())
    if customText == False:
        print("📝 Please select one of the following options:")
    else:
        print(customText)
    for id, item in enumerate(options, start=1):
        print(f"{number_emoji_mapping[id]} {item}")

    passed = False
    while not passed:
        userin = user_input("integer")
        if (userin < 1) or (userin > len(options)):
            print("⚠️ Please enter a valid option.")
        elif go_back_allowed and userin == len(options):
            return len(options)
        else:
            return userin


def user_input(type_needed, message = False):
    type_needed = type_needed.lower()
    passed = False
    while not passed:
        if message != False:
            print(message)

        userInput = input()
        if type_needed == "integer":
            try:
                userInput = int(userInput)
                passed = True
            except ValueError:
                print("🔢 Please enter a number.")
        elif type_needed == "string":
            try:
                userInput = int(userInput)
                print("✏️ Please enter a string.")
            except ValueError:
                passed = True
    return userInput


def view_stadium_menu(stadiumID, stadium, game):
    clubs = game.getClubs()

    print(seperator())
    print(f"️🏟️ {stadium.getName()}")
    print(seperator())
    print(f"📅 Opened: {stadium.getOpenedDate()}")
    print(f"👥 Capacity: {stadium.getCapacity()}")
    print(f"📍 City: {stadium.getCity()}")
    print(f"🛡️ Club: {clubs[stadium.getClub()].getShortName()}")
    ui = option_menu([f"View {clubs[stadium.getClub()].getShortName()}"], go_back_allowed = True)
    if ui == 1:
        clubID = stadium.getClub()
        club = clubs[clubID]
        view_club_menu(clubID, club, game)
    elif ui == 2:
        return


def view_manager_menu(managerID, manager, game):

    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    print(seperator())
    print(f"️🧑‍💼 {manager.getName()} | {clubs[manager.getClub()].getFullName()}")
    print(seperator())
    print(f"Age: {manager.getAge()}")
    print(f"Nationality: {nations[manager.getNationality()].getName()}")
    ui = option_menu([f"View {clubs[manager.getClub()].getShortName()}"], go_back_allowed = True)
    if ui == 1:
        clubID = manager.getClub()
        club = clubs[clubID]
        view_club_menu(clubID, club, game)
    elif ui == 2:
        return

def view_free_agents_menu(clubID, club, game):
    print(seperator())
    print(f"️🛡️️ {club.getFullName()}")
    print(seperator())
    print(f"⛹️ Players unemployed: {len(club.getPlayers())}")
    print(f"🧑‍💼 Managers unemployed: {len(club.getManagers())}")
    ui = option_menu(["View free agent players", "View free agent managers"], go_back_allowed = True)
    if ui == 1:
        page = 1
        settings = {"Free Agents Only": True}
        player_database_menu(game, page, settings)
    elif ui == 2:
        page = 1
        settings = {"Free Agents Only": True}
        staff_database_menu(game, page, settings)
    elif ui == 3:
        return


def view_club_fixtures(clubID, club, game):

    month_mapping = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    leagues = game.getLeagues()
    fixtures = club.getFixtures()
    print(seperator())
    print(f"️🛡️️ {club.getFullName()}'s Fixtures")
    print(seperator())
    previous_month = None
    for fixture in fixtures:
        monthUpdated = False
        day, month, year = fixture.getDate()
        fixtureMonth = int(month)
        if previous_month != month:
            previous_month = month
            month = fixtureMonth
            monthUpdated = True
        if monthUpdated:
            print("")
            print(f"🔹 {month_mapping[month].upper()} 🔹")

        home, away = fixture.getTeams()

        league = leagues[fixture.getLeagueID()]
        if fixture.getScore() is not None:
            hScore, aScore = fixture.getScore()

        if fixture.getScore() is not None and fixture.getType() == "league":
            print(f"{league.getName()} | {day}/{month}/{year} | {home.getShortName()} {hScore} - {away.getShortName()} {aScore}")
        elif fixture.getScore() is not None and fixture.getType() == "knockout" and fixture.getTournamentID() is None:
            print(f"{league.getName()} | {fixture.getStage()} | {day}/{month}/{year} | {home.getShortName()} {hScore} - {away.getShortName()} {aScore}")
        elif fixture.getScore() is None and fixture.getType() == "league":
            print(f"{league.getName()} | {day}/{month}/{year} | {home.getShortName()} - {away.getShortName()}")
        elif fixture.getScore() is None and fixture.getType() == "knockout" and fixture.getTournamentID() is None:
            print(f"{league.getName()} | {fixture.getStage()} | {day}/{month}/{year} | {home.getShortName()} - {away.getShortName()}")

    ui = option_menu([f"View {club.getFullName()}"], go_back_allowed=True)
    if ui == 1:
        view_club_menu(clubID, club, game)
    elif ui == 2:
        return

def view_league_menu(leagueID, league, game, sort="points"):

    nations = game.getNations()
    nationObject = nations[league.getNation()]

    print(seperator())
    print(f"️🛡️️ {league.getName()} - {nationObject.getName()}")
    print(seperator())

    clubs = league.getClubs()
    clubList = []

    for club in clubs.values():
        clubList.append(club)

    if sort == "points":
        clubList.sort(key=lambda club: (-club.getPoints(), -club.getGoalDifference(), -club.getGoalsFor(), club.getFullName()))
    elif sort == "gamesPlayed":
        clubList.sort(key=lambda p: p.getMatchesPlayed(), reverse=True)
    elif sort == "goalDifference":
        clubList.sort(key=lambda p: p.getGoalDifference(), reverse=True)
    elif sort == "mediaPrediction":
        clubList.sort(key=lambda p: p.calculateBettingOdds(game))

    print("Club Name | Games Played | Wins | Draws | Losses | Goal Difference | Points")
    print(seperator())
    if sort == "mediaPrediction":
        for club in clubList:
            print(f"{club.getFullName()} - {club.calculateBettingOdds(game)}/1")
    else:
        for club in clubList:
            print(f"{club.getFullName()} - {club.getMatchesPlayed()} Pl - {club.getWins()} W - {club.getDraws()} D - {club.getLosses()} L - {club.getGoalDifference()} GD - {club.getPoints()} Pts")

    ui = option_menu([f"View club in {league.getName()}", "Sort by points", "Sort by games played", "Sort by goal difference", "Sort by Media Prediction"], True)
    if ui == 1:
        tempDict = {}
        for club in clubList:
            tempDict[club.getID()] = club
        clubDict = tempDict
        clubID, club = search(clubDict)
        view_club_menu(clubID, club, game)
    elif ui == 2:
        view_league_menu(leagueID, league, game, sort="points")
    elif ui == 3:
        view_league_menu(leagueID, league, game, sort="gamesPlayed")
    elif ui == 4:
        view_league_menu(leagueID, league, game, sort="goalDifference")
    elif ui == 5:
        view_league_menu(leagueID, league, game, sort="mediaPrediction")
    elif ui == 6:
        return


def view_club_menu(clubID, club, game):
    leagues = game.getLeagues()
    managers = game.getManagers()
    clubs = game.getClubs()

    leagueID = club.getLeague()
    leagueObject = leagues[leagueID]

    playerManagerID = len(managers)
    playerManagerClubID = clubs[managers[playerManagerID].getClub()].getID()

    if clubID == 0:
        view_free_agents_menu(clubID, club, game)
        return

    print(seperator())
    print(f"️🛡️️ {club.getFullName()} {club.printColors()}")
    print(seperator())
    print("📖 About Club")
    print(f"Founded: {club.getFoundedDate()}")
    print(f"Nickname: {club.getNickname()}")
    print("")
    print("📈 Club Finances")
    print(f"Transfer Budget: {club.getTransferBudget()}")
    print(f"Total Player Wages: £{club.getTotalPlayerWages()}")
    print("")
    print("🧑‍💼 Manager")
    print(f"Name: {club.getManager().getName()}")
    print("")
    print("🏟️ Stadium")
    print(f"Name: {club.getStadium().getName()}")

    ui = option_menu([f"View {club.getFullName()} Squad", f"View {leagueObject.getName()}", f"View {club.getShortName()}'s Fixtures", f"View {club.getManager().getName()}", f"View {club.getStadium().getName()}"], True)
    if ui == 1:
        if clubs[playerManagerClubID] == club:
            view_squad_screen(clubID, game, sort="position")
        else:
            page = 1
            settings = {"Club": club.getShortName()}
            player_database_menu(game, page, settings)
    elif ui == 2:
        view_league_menu(leagueID, leagueObject, game)
    elif ui == 3:
        view_club_fixtures(clubID, club, game)
    elif ui == 4:
        managerID = club.getManager().getID()
        view_manager_menu(managerID, club.getManager(), game)
    elif ui == 5:
        stadiumID = club.getStadium().getID()
        view_stadium_menu(stadiumID, club.getStadium(), game)
    elif ui == 6:
        return

def player_transfer_menu(playerID, player, game):

    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    playerManagerID = len(managers)
    playerManagerObject = managers[playerManagerID]
    playerManagerClubID = clubs[managers[playerManagerID].getClub()].getID()

    print(seperator())
    print(f"️‍⛹️‍♂️ {player.getName()} | Transfer Options")

    if player in playerManagerObject.getShortlist():
        shortlisted = True
    else:
        shortlisted = False

    if player in clubs[playerManagerClubID].getPlayers():
        selfPlayer = True
    else:
        selfPlayer = False

    if not selfPlayer:
        print(seperator())
        print(f"Shortlisted: {shortlisted}")

    if selfPlayer:
        ui = option_menu(["Enter Contract Negotiations"], go_back_allowed=True)
        if ui == 1:
            print("Contract Negotiations")
        elif ui == 2:
            view_player_menu(playerID, player, game)
    if not selfPlayer:
        ui = option_menu(["Approach to buy", "Toggle Shortlist"], go_back_allowed=True)
        if ui == 1:
            print("Approach to buy")
        elif ui == 2:
            if shortlisted:
                shortlist = playerManagerObject.getShortlist()
                shortlist.remove(player)
            elif not shortlisted:
                shortlist = playerManagerObject.getShortlist()
                shortlist.append(player)
            player_transfer_menu(playerID, player, game)
        elif ui == 3:
            view_player_menu(playerID, player, game)


def view_player_menu(playerID, player, game):

    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    playerManagerID = len(managers)
    playerManagerClubID = clubs[managers[playerManagerID].getClub()].getID()
    if playerManagerClubID != 0:
        playersListForStarRating = clubs[playerManagerClubID].getFirstTeam()
    else:
        playersListForStarRating = players


    print(seperator())
    print(f"️‍⛹️‍♂️ {player.getName()} | Age: {player.getAge(dateObject)} ({player.getBirthday()}) | {nations[player.getNationality()].getName()}")
    print(f"{player.getPosition().getName()} | {clubs[player.getClub()].getFullName()} {clubs[player.getClub()].printColors()} | {player.calculateRating()} | Rating: {player.calculateStarRating(playersListForStarRating)}")
    print(seperator())
    (passing, dribbling, finishing, defending, ball_control, delivery, vision, football_iq, positioning, composure, decision_making, work_rate, aggression,
     pace, strength, stamina, aerial, shot_stopping, handling, distribution, command)= player.getAttributes()
    print("📊 Attributes:")
    if player.getPosition().getAbbreviation() == "GK":
        print(f"Shot Stopping: {shot_stopping}")
        print(f"Handling: {handling}")
        print(f"Distribution: {distribution}")
        print(f"Command: {command}")
    else:
        print("")
        print("⚽ TECHNICAL:")
        print(f"Finishing: {finishing}")
        print(f"Delivery: {delivery}")
        print(f"Passing: {passing}")
        print(f"Dribbling: {dribbling}")
        print(f"Ball Control: {ball_control}")
        print(f"Defending: {defending}")
        print("")
        print("🧠 MENTAL:")
        print(f"Vision: {vision}")
        print(f"Decision Making: {decision_making}")
        print(f"Composure: {composure}")
        print(f"Football IQ: {football_iq}")
        print(f"Positioning: {positioning}")
        print(f"Aggression: {aggression}")
        print(f"Work Rate: {work_rate}")
        print("")
        print("💪 PHYSICAL:")
        print(f"Pace: {pace}")
        print(f"Strength: {strength}")
        print(f"Stamina: {stamina}")
        print(f"Aerial: {aerial}")

    if player.getClub() != 0:
        print("")
        print("🛡️ Club:")
        print(f"Club: {clubs[player.getClub()].getFullName()}")
        print(f"Wage: £{player.getCurrentWage()} per week")
        print(f"Contract Length: {player.getContractLength()} years remaining")

    clubID = player.getClub()
    club = clubs[clubID]

    ui = option_menu([f"View {clubs[player.getClub()].getFullName()}", "Transfer Options"], go_back_allowed = True)
    if ui == 1:
        view_club_menu(clubID, club, game)
    elif ui == 2:
        player_transfer_menu(playerID, player, game)
    elif ui == 3:
        return


def database_view_settings_menu(game, settings):
    clubs = game.getClubs()
    print(seperator())
    print(f"Player Database View Filters Menu")
    if len(settings) != 0:
        print(seperator())
        for key, setting in settings.items():
            print(f"{key}: {setting}")
    ui = option_menu(["Add Age Restriction", "Free Agents Only", "Club", "Clear All"], go_back_allowed = True)
    if ui == 1:
        min_age = user_input("integer", "Minimum Age Restriction:")
        max_age = user_input("integer", "Maximum Age Restriction:")
        settings["Minimum Age Restriction"] = min_age
        settings["Maximum Age Restriction"] = max_age
        return settings
    elif ui == 2:
        settings["Free Agents Only"] = True
        return settings
    elif ui == 3:
        clubID, club = search(clubs)
        settings["Club"] = club.getShortName()
        return settings
    elif ui == 4:
        settings = {}
        return settings
    elif ui == 5:
        return settings

def player_database_menu(game, page = 1, settings = {}):

    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    playerManagerID = len(managers)
    playerManagerObject = managers[playerManagerID]
    playerManagerClubID = clubs[managers[playerManagerID].getClub()].getID()
    ClubObject = clubs[playerManagerClubID]

    clubPlayers = ClubObject.getFirstTeam()

    playerList = []

    for player in players.values():
        playerList.append(player)

    playerList.sort(key=lambda p: p.calculateRating(), reverse = True)

    # APPLYING FILTERS
    players_to_remove = []
    if "Minimum Age Restriction" in settings.keys():
        for player in playerList:
            if player.getAge(dateObject) < settings["Minimum Age Restriction"]:
                players_to_remove.append(player)
    if "Maximum Age Restriction" in settings.keys():
        for player in playerList:
            if player.getAge(dateObject) > settings["Maximum Age Restriction"]:
                players_to_remove.append(player)
    if "Free Agents Only" in settings.keys():
        for player in playerList:
            if player.getClub() != 0:
                players_to_remove.append(player)
    if "Player Shortlist" in settings.keys():
        for player in playerList:
            if player not in playerManagerObject.getShortlist():
                players_to_remove.append(player)
    if "Club" in settings.keys():
        for player in playerList:
            if clubs[player.getClub()].getShortName() != settings["Club"]:
                players_to_remove.append(player)

    for player in players_to_remove:
        if player in playerList:
            playerList.remove(player)


    print(seperator())
    print(f"Player Database View: Page {[page]} | Total: {len(playerList)}")
    print(seperator())
    print("Star Rating | Approx. Value | Pos | Club | Nation | Age | Name")
    print(seperator())

    pageStart = ((page - 1) * 20) + 1
    pageEnd = page * 20

    playersOnPage = []

    for player in playerList[pageStart-1:pageEnd]:
        playersOnPage.append(player)
        print(f"{player.calculateStarRating(clubPlayers)} | {player.calculateMarketValue(game)} "
              f"| {player.getPosition()} | {clubs[player.getClub()].getShortName()} | {nations[player.getNationality()].getAbbreviation()} | {player.getAge(dateObject)} | {player.getName()} | {player.calculateRating()}")

    ui = option_menu(["Previous Page", "Next Page", "Search for player on page", "Filters"], go_back_allowed=True)
    if ui == 1:
        if page != 1:
            page -= 1
        player_database_menu(game, page, settings)
    elif ui == 2:
        page += 1
        player_database_menu(game, page, settings)
    elif ui == 3:
        tempDict = {}
        for player in playersOnPage:
            tempDict[player.getID()] = player
        playersOnPage = tempDict
        playerID, player = search(playersOnPage)
        view_player_menu(playerID, player, game)
    elif ui == 4:
        settings = database_view_settings_menu(game, settings)
        player_database_menu(game, page, settings)
    elif ui == 5:
        recruitment_menu(game)


def staff_database_menu(game, page = 1, settings = {}):

    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    staffList = []

    for manager in managers.values():
        staffList.append(manager)

    staffList.sort(key = lambda manager: manager.getSurname())

    print(seperator())
    print(f"Player Database View: Page {[page]} | Total: {len(staffList)}")
    print(seperator())
    print("Star Rating | Pos | Club | Nation | Age | Name")
    print(seperator())

    pageStart = ((page - 1) * 20) + 1
    pageEnd = page * 20

    staffOnPage = []

    for staff in staffList[pageStart-1:pageEnd]:
        staffOnPage.append(staff)
        print(f"{clubs[staff.getClub()].getShortName()} | {nations[staff.getNationality()].getAbbreviation()} | {staff.getAge()} | {staff.getName()}")

    ui = option_menu(["Previous Page", "Next Page", "Search for manager on page"], go_back_allowed=True)
    if ui == 1:
        if page != 1:
            page -= 1
        staff_database_menu(game, page, settings)
    elif ui == 2:
        page += 1
        staff_database_menu(game, page, settings)
    elif ui == 3:
        tempDict = {}
        for staff in staffOnPage:
            tempDict[staff.getID()] = staff
        staffOnPage = tempDict
        managerID, manager = search(staffOnPage)
        view_manager_menu(managerID, manager, game)
    elif ui == 4:
        recruitment_menu(game)

def team_sheet_menu(clubID, club, game):
    positions = game.getPositions()
    players = club.getPlayers()
    clubs = game.getClubs()

    print(seperator())
    print(f"{clubs[clubID].printColors()} {clubs[clubID].getFullName()}'s Squad")
    print(seperator())
    formation, starting_eleven, bench = club.getTeamSheet()

    if formation is not None and len(starting_eleven) > 0 and len(bench) > 0:
        for index, position in enumerate(formation):
            print(f"{starting_eleven[index].calculateStarRating(players)} | {positions[position].getAbbreviation()} | {starting_eleven[index].getName()}")
        for index, player in enumerate(bench):
            print(f"{player.calculateStarRating(players)} | Bench | {player.getName()}")


    ui = option_menu(["Auto Pick Team", "Set Formation", "Clear Team Sheet"], go_back_allowed=True)
    if ui == 1:
        formation, starting_eleven, bench = club.autoPickTeam()
        club.setTeamSheet(formation, starting_eleven, bench)
        team_sheet_menu(clubID, club, game)
    elif ui == 2:
        print("")
    elif ui == 3:
        formation = None
        starting_eleven = []
        bench = []
        club.setTeamSheet(formation, starting_eleven, bench)
        team_sheet_menu(clubID, club, game)
    elif ui == 4:
        return



def view_squad_screen(clubID, game, sort = "position", type = "firstTeam"):
    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    print(seperator())
    print(f"{clubs[clubID].printColors()} {clubs[clubID].getFullName()}'s Squad")
    print(seperator())
    clubPlayers = clubs[clubID].getPlayers()
    firstTeam = clubs[clubID].getFirstTeam()

    if type == "firstTeam":
        clubPlayers = clubs[clubID].getFirstTeam()
    elif type == "youthTeam":
        clubPlayers = clubs[clubID].getYouthTeam()

    if sort == "rating":
        clubPlayers.sort(key=lambda p: p.calculateRating(), reverse = True)
    elif sort == "position":
        clubPlayers.sort(key=lambda p: p.getPosition().getID())
    elif sort == "age":
        clubPlayers.sort(key=lambda p: p.getAge(dateObject))

    print("Star Rating | Pos | Nation | Age | Name")
    print(seperator())
    for player in clubPlayers:
        print(f"{player.calculateStarRating(firstTeam)} | {player.getPosition()} | {nations[player.getNationality()].getAbbreviation()} | {player.getAge(dateObject)} | {player.getName()}")
    ui = option_menu([f"View {clubs[clubID].getShortName()} First Team", f"View {clubs[clubID].getShortName()} Youth Squad", "Sort players by rating", "Sort players by position", "Sort players by age", "View a player in squad"], go_back_allowed=True)
    if ui == 1:
        view_squad_screen(clubID, game, sort="position", type = "firstTeam")
    elif ui == 2:
        view_squad_screen(clubID, game, sort="position", type = "youthTeam")
    elif ui == 3:
        view_squad_screen(clubID, game, sort="rating", type=type)
    elif ui == 4:
        view_squad_screen(clubID, game, sort="position", type=type)
    elif ui == 5:
        view_squad_screen(clubID, game, sort="age", type=type)
    elif ui == 6:
        tempDict = {}
        for player in clubPlayers:
            tempDict[player.getID()] = player
        clubPlayers = tempDict
        playerID, player = search(clubPlayers)
        view_player_menu(playerID, player, game)
    elif ui == 7:
        return

def universal_search_menu(game):
    ui = option_menu(["⛹️‍♂️ Players", "🛡️ Clubs", "📜 Leagues", "🧑‍💼 Managers", "🏟 Stadiums"], go_back_allowed=True)
    if ui == 1:
        players = game.getPlayers()
        playerID, player = search(players)
        view_player_menu(playerID, player, game)
    elif ui == 2:
        clubs = game.getClubs()
        clubID, club = search(clubs)
        view_club_menu(clubID, club, game)
    elif ui == 3:
        leagues = game.getLeagues()
        leagueID, league = search(leagues)
        view_league_menu(leagueID, league, game)
    elif ui == 4:
        managers = game.getManagers()
        managerID, manager = search(managers)
        view_manager_menu(managerID, manager, game)
    elif ui == 5:
        stadiums = game.getStadiums()
        stadiumID, stadium = search(stadiums)
        view_stadium_menu(stadiumID, stadium, game)
    elif ui == 6:
        return


def recruitment_menu(game):
    print(seperator())
    print(f"🖊️ Recruitment Hub")
    ui = option_menu(["View Player Database", "View Manager Database", "View Player Shortlist"], go_back_allowed=True)
    if ui == 1:
        player_database_menu(game)
    elif ui == 2:
        staff_database_menu(game)
    elif ui == 3:
        page = 1
        settings = {
            "Player Shortlist": True
        }
        player_database_menu(game, page, settings)
    elif ui == 4:
        return

def holiday_menu(game):
    dateObject = game.getDateObject()
    gameDay, gameMonth, gameYear = dateObject.getDate()

    day = None
    month = None
    year = None
    while True:
        ui = option_menu(["Day", "Month", "Year", "Go On Holiday"], True, "📅 Let's select what date to holiday until:")
        if ui == 1:
            passed = False
            while not passed:
                day = user_input("integer", "Enter day of date to holiday until: (1-31)")
                if 0 < day <= 31:
                    passed = True
                else:
                    print("🚫 Invalid day!")
            print(f"✅ Day set to {day} of the month!")
        elif ui == 2:
            passed = False
            while not passed:
                month = user_input("integer", "Enter month of date to holiday until: (1-12)")
                if 0 < month <= 12:
                    passed = True
                else:
                    print("🚫 Invalid month!")
            print(f"✅ Month of year set to {month}!")
        elif ui == 3:
            passed = False
            while not passed:
                year = user_input("integer", "Enter year of date to holiday until: ")
                if 2024 < year <= 5000:
                    passed = True
                else:
                    print("🚫 Invalid year!")
            print(f"✅ Year set to {year}!")
        elif ui == 4:
            if day is not None and month is not None and year is not None and dateObject.validDateChecker(day, month, year) is True and dateObject.isInFutureChecker(day, month, year) is True:

                return day, month, year
            else:
                print("🚫 All fields are not completed or you have chosen an invalid date!")
        elif ui == 5:
            return

def game_main_menu(game):
    while True:
        dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

        playerManagerID = len(managers)
        playerManagerClubID = clubs[managers[playerManagerID].getClub()].getID()
        clubObject = clubs[playerManagerClubID]


        day, month, year = dateObject.getDate()

        if len(clubObject.getFixtures()) == 0:
            next_fixture = None
        else:
            for fixture in clubObject.getFixtures():
                if fixture.getScore() is None:
                    next_fixture = fixture
                    home, away = fixture.getTeams()
                    if home == clubObject:
                        opposition = away
                    elif away == clubObject:
                        opposition = home
                    d, m, y = fixture.getDate()
                    break
                else:
                    next_fixture = None

        print(seperator())
        print(f"{dateObject.getWeekday()} | {day}/{month}/{year} - {managers[playerManagerID].getName()} - {clubs[playerManagerClubID].getFullName()} {clubs[playerManagerClubID].printColors()}")
        if next_fixture is not None:
            print(f"➡️ Next Match: {opposition.getName()} | {d}/{m}/{y}")
        ui = option_menu(["Advance", f"View {clubs[playerManagerClubID].getShortName()} Team Sheet", f"View {clubs[playerManagerClubID].getShortName()} First Team Squad", f"View {clubs[playerManagerClubID].getShortName()} Club Site",
                          f"View {clubs[playerManagerClubID].getShortName()}'s Fixtures", "Universal Search", "Recruitment Hub", "Go On Holiday", "Return to main menu"])
        if ui == 1:
            return "Advance"
        elif ui == 2:
            team_sheet_menu(playerManagerClubID, clubs[playerManagerClubID], game)
        elif ui == 3:
            view_squad_screen(playerManagerClubID, game)
        elif ui == 4:
            view_club_menu(playerManagerClubID, clubs[playerManagerClubID], game)
        elif ui == 5:
            view_club_fixtures(playerManagerClubID, clubs[playerManagerClubID], game)
        elif ui == 6:
            universal_search_menu(game)
        elif ui == 7:
            recruitment_menu(game)
        elif ui == 8:
            returnValue = holiday_menu(game)
            if returnValue is not None:
                day, month, year = returnValue
                game.arrangeHoliday(day, month, year)
                return None
        elif ui == 9:
            return "Return to main menu"



