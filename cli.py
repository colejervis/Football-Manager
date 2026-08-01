from classes import seasonData


def safe_divide(numerator, denominator):
    return numerator / denominator if denominator else 0

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

def fixture_search(fixtures, game):
    while True:

        clubs = game.getClubs()

        print("Home Club:")
        homeClubID, homeClub = search(clubs)
        print("Away Club:")
        awayClubID, awayClub = search(clubs)

        SearchEntries = []

        for fixture in fixtures:
            homeTeam, awayTeam = fixture.getTeams()
            if homeTeam == homeClub and awayTeam == awayClub:
                SearchEntries.append(fixture)

        if len(SearchEntries) == 0:
            print(f"❌ no fixtures found for {homeClub} vs {awayClub}!")
        elif len(SearchEntries) == 1:
            for fixture in SearchEntries:
                return fixture
        else:
            print(f"Found {len(SearchEntries)} search results:")
            SearchEntriesList = []
            for fixture in SearchEntries:
                SearchEntriesList.append(fixture)
            for position, fixture in enumerate(SearchEntriesList, start=1):
                homeTeam, awayTeam = fixture.getTeams()
                day, month, year = fixture.getDate()
                if fixture.getScore() is None:
                    print(f"{position} | {homeTeam.getName()} - {awayTeam.getName()} | {day}/{month}/{year}")
                else:
                    homeScore, awayScore = fixture.getScore()
                    print(f"{position} | {homeTeam.getName()} {homeScore} - {awayTeam.getName()} {awayScore} | {day}/{month}/{year}")
            passed = False
            while not passed:
                userInput = input("🔢 Please select the number corresponding to which item you want to select: ")
                try:
                    userInput = int(userInput) - 1
                    passed = True
                except ValueError:
                    print("🔢 Please enter a number.")

            selectedItem = SearchEntriesList[userInput]
            return selectedItem

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
        10: "1️⃣0️⃣",
        11: "1️⃣1️⃣",
        12: "1️⃣2️⃣",
        13: "1️⃣3️⃣",
        14: "1️⃣4️⃣",
        15: "1️⃣5️⃣",
        16: "1️⃣6️⃣",
        17: "1️⃣7️⃣",
        18: "1️⃣8️⃣",
        19: "1️⃣9️⃣",
        20: "2️⃣0️⃣",
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

def view_fixture_menu(fixture, game):
    homeTeam, awayTeam = fixture.getTeams()

    events = fixture.getMatchEvents()
    matchStatistics = fixture.getMatchStatistics()

    if fixture.getScore() is not None:
        homeScore, awayScore = fixture.getScore()

        print(seperator())
        print(f"⚽ MATCH REPORT - {homeTeam.getFullName()} {homeScore} - {awayScore} {awayTeam.getFullName()}")
        if fixture.getPenaltyScore() is not None:
            homePenalty, awayPenalty = fixture.getPenaltyScore()
            print(f"{homeTeam.getFullName()} {homePenalty} - {awayPenalty} {awayTeam.getFullName()} on penalties")
        print(seperator())


        print(f"🤝 Possession: {homeTeam.getShortName()} {matchStatistics['homePossession']}% - {awayTeam.getShortName()} {matchStatistics['awayPossession']}%")
        print(f"🥾 Passes: {homeTeam.getShortName()} {matchStatistics['homePasses']} - {awayTeam.getShortName()} {matchStatistics['awayPasses']}")
        print(f"🎯 Shots: {homeTeam.getShortName()} {matchStatistics['homeShots']} - {awayTeam.getShortName()} {matchStatistics['awayShots']}")
        print(f"🥅 Big Chances: {homeTeam.getShortName()} {matchStatistics['homeBigChances']} - {awayTeam.getShortName()} {matchStatistics['awayBigChances']}")
        print(f"📊 Expected Goals: {homeTeam.getShortName()} {matchStatistics['homeXG']} - {awayTeam.getShortName()} {matchStatistics['awayXG']}")
        print(f"🧑‍⚖️ Fouls: {homeTeam.getShortName()} {matchStatistics['homeFouls']} - {awayTeam.getShortName()} {matchStatistics['awayFouls']}")
        print(f"🟨 Yellow Cards: {homeTeam.getShortName()} {matchStatistics['homeYellowCards']} - {awayTeam.getShortName()} {matchStatistics['awayYellowCards']}")
        print(f"🟥 Red Cards: {homeTeam.getShortName()} {matchStatistics['homeRedCards']} - {awayTeam.getShortName()} {matchStatistics['awayRedCards']}")
        print(seperator())
        # Sort by minute
        events.sort(key=lambda event: event["minute"])

        for event in events:
            minute = event["minute"]
            team = event["team"].getShortName()

            if event["type"] == "chance":
                if event["outcome"] == "goal":
                    scorer = event["scorer"].getName()

                    if event["assister"] is not None:
                        assister = event["assister"].getName()
                        print(f"{minute}' ⚽ {team} | {scorer} (Assist: {assister})")
                    else:
                        print(f"{minute}' ⚽ {team} | {scorer}")

            elif event["type"] == "foul":
                player = event["player"].getName()

                if event["outcome"] == "yellow":
                    print(f"{minute}' 🟨 {team} | {player}")

                elif event["outcome"] == "red":
                    print(f"{minute}' 🟥 {team} | {player}")

            elif event["type"] == "substitution":
                outgoing = event["leaving-match"].getName()
                incoming = event["joining-match"].getName()
                print(f"{minute}' 🔄 {team} | 🛑 {outgoing} | 🟢️ {incoming}")

            elif event["type"] == "injury":
                player = event["player"].getName()
                print(f"{minute}' 🚑 {team} | {player}")

            elif event["type"] == "penalty":
                player = event["taker"].getName()
                if event["outcome"] == "scored":
                    print(f"Penalty: ✅ {team} | {player}")
                elif event["outcome"] == "missed":
                    print(f"Penalty: ❌ {team} | {player}")
    else:
        print("⚠️ Fixture has not been played yet.")

    ui = option_menu([f"View {homeTeam.getName()}", f"View {awayTeam.getName()}"], go_back_allowed=True)
    if ui == 1:
        view_club_menu(homeTeam.getID(), homeTeam, game)
    elif ui == 2:
        view_club_menu(awayTeam.getID(), awayTeam, game)
    elif ui == 3:
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

    ui = option_menu([f"View {club.getFullName()}", "View a fixture"], go_back_allowed=True)
    if ui == 1:
        view_club_menu(clubID, club, game)
    elif ui == 2:
        clubFixtures = club.getFixtures()
        for clubFixture in clubFixtures:
            if clubFixture not in fixtures:
                fixtures.append(clubFixture)

        fixture = fixture_search(fixtures, game)
        view_fixture_menu(fixture, game)
    elif ui == 3:
        return

def view_league_menu(leagueID, league, game, sort="points"):

    nations = game.getNations()
    nationObject = nations[league.getNation()]

    print(seperator())
    print(f"🛡️ {league.getName()} - {nationObject.getName()}")
    print(seperator())

    clubList = list(league.getClubs().values())

    sort_functions = {
        "points": (lambda c: (-c.getPoints(), -c.getGoalDifference(), -c.getGoalsFor(), c.getFullName()), "Normal"),
        "gamesPlayed": (lambda c: c.getMatchesPlayed(), "Normal"),
        "goalDifference": (lambda c: c.getGoalDifference(), "Normal"),
        "goalsScored": (lambda c: c.leagueGoalsFor, "Data"),
        "goalsConceded": (lambda c: c.leagueGoalsAgainst, "Data"),
        "cleanSheets": (lambda c: c.leagueCleanSheets, "Data"),
        "averagePossession": (lambda c: safe_divide(c.leagueTotalPossession, c.leagueMatchesPlayed), "Data"),
        "passesPer90": (lambda c: safe_divide(c.leagueTotalPasses, c.leagueMatchesPlayed), "Data"),
        "shotsPer90": (lambda c: safe_divide(c.leagueTotalShots, c.leagueMatchesPlayed), "Data"),
        "bigChancesPer90": (lambda c: safe_divide(c.leagueTotalBigChances, c.leagueMatchesPlayed), "Data"),
        "xgTotal": (lambda c: c.leagueTotalXG, "Data"),
        "xgPer90": (lambda c: safe_divide(c.leagueTotalXG, c.leagueMatchesPlayed), "Data"),
        "fouls": (lambda c: c.leagueTotalFouls, "Data"),
        "yellowCards": (lambda c: c.leagueTotalYellowCards, "Data"),
        "redCards": (lambda c: c.leagueTotalRedCards, "Data"),
        "mediaPrediction": (lambda c: c.calculateBettingOdds(game), "Media Prediction")
    }

    sort_key, view = sort_functions[sort]
    clubList.sort(key=sort_key, reverse=(sort != "points" and sort != "mediaPrediction"))

    if view == "Normal":

        print("Pos | Club | Pl | W | D | L | GD | Pts")
        print(seperator())

        for pos, club in enumerate(clubList, start=1):
            print(
                f"{pos}. {club.getFullName()} - "
                f"{club.getMatchesPlayed()} Pl - "
                f"{club.getWins()} W - "
                f"{club.getDraws()} D - "
                f"{club.getLosses()} L - "
                f"{club.getGoalDifference()} GD - "
                f"{club.getPoints()} Pts"
            )

    elif view == "Media Prediction":

        print("Pos | Club | Odds")
        print(seperator())

        for pos, club in enumerate(clubList, start=1):
            print(f"{pos}. {club.getFullName()} - {club.calculateBettingOdds(game)}/1")

    else:

        headers = {
            "goalsScored": "Goals",
            "goalsConceded": "Goals Against",
            "cleanSheets": "Clean Sheets",
            "averagePossession": "Possession %",
            "passesPer90": "Passes / 90",
            "shotsPer90": "Shots / 90",
            "bigChancesPer90": "Big Chances / 90",
            "xgTotal": "Total XG",
            "xgPer90": "xG / 90",
            "fouls": "Fouls /90",
            "yellowCards": "Yellow Cards",
            "redCards": "Red Cards",
        }

        print(f"Pos | Club | {headers[sort]}")
        print(seperator())

        value_functions = {
            "goalsScored": lambda c: c.leagueGoalsFor,
            "goalsConceded": lambda c: c.leagueGoalsAgainst,
            "cleanSheets": lambda c: c.leagueCleanSheets,
            "averagePossession": lambda c: f"{safe_divide(c.leagueTotalPossession, c.leagueMatchesPlayed):.1f}%",
            "passesPer90": lambda c: f"{safe_divide(c.leagueTotalPasses, c.leagueMatchesPlayed):.1f}",
            "shotsPer90": lambda c: f"{safe_divide(c.leagueTotalShots, c.leagueMatchesPlayed):.1f}",
            "bigChancesPer90": lambda c: f"{safe_divide(c.leagueTotalBigChances, c.leagueMatchesPlayed):.1f}",
            "xgTotal": lambda c: f"{c.leagueTotalXG:.1f}",
            "xgPer90": lambda c: f"{safe_divide(c.leagueTotalXG, c.leagueMatchesPlayed):.2f}",
            "fouls": lambda c: c.leagueTotalFouls,
            "yellowCards": lambda c: c.leagueTotalYellowCards,
            "redCards": lambda c: c.leagueTotalRedCards,
            "mediaPrediction": lambda c: c.calculateBettingOdds(game)
        }

        get_value = value_functions[sort]

        for pos, club in enumerate(clubList, start=1):
            print(f"{pos}. {club.getFullName()} - {get_value(club)}")

    ui = option_menu(
        ["View club in league", "Sort Menu", "View player stats", "View Media Prediction"],
        True
    )

    if ui == 1:
        clubDict = {club.getID(): club for club in clubList}
        clubID, club = search(clubDict)
        view_club_menu(clubID, club, game)

    elif ui == 2:
        modifiedSort = league_sort_menu(game, leagueID, league, sort)
        view_league_menu(leagueID, league, game, modifiedSort)

    elif ui == 3:
        league_player_stats_menu(leagueID, league, game, sort="goals")

    elif ui == 4:
        view_league_menu(leagueID, league, game, "mediaPrediction")

    elif ui == 4:
        return

def league_player_stats_menu(leagueID, league, game, sort="goals"):
    players = game.getPlayers()
    print(seperator())
    print(f"🛡️ {league.getName()}")
    print(seperator())
    players_in_league = []
    for player in players.values():
        for playerLeagueID in player.seasonData.keys():
            if playerLeagueID == leagueID:
                players_in_league.append(player)

    if sort == "goals":
        players_in_league.sort(key=lambda p: p.seasonData[leagueID].goals, reverse=True)
    elif sort == "assists":
        players_in_league.sort(key=lambda p: p.seasonData[leagueID].assists, reverse=True)
    elif sort == "goalsContributions":
        players_in_league.sort(key=lambda p: p.seasonData[leagueID].goals + p.seasonData[leagueID].assists)
    elif sort == "yellowCards":
        players_in_league.sort(key=lambda p: p.seasonData[leagueID].yellowCards, reverse=True)
    elif sort == "redCards":
        players_in_league.sort(key=lambda p: p.seasonData[leagueID].redCards, reverse=True)
    elif sort == "cleanSheets":
        players_in_league.sort(key=lambda p: p.seasonData[leagueID].cleanSheets, reverse=True)

    players_to_show = []

    if len(players_in_league) > 9:
        for i in range(10):
            players_to_show.append(players_in_league[i])
    elif len(players_in_league) < 10:
        for i in range(len(players_in_league)):
            players_to_show.append(players_in_league[i])


    print("Name | Pos | Goals | Assists | Yellow Cards | Red Cards | Clean Sheets")
    print(seperator())
    for player in players_to_show:
        print(f"{player.getName()} - {player.getPosition()} - {player.seasonData[leagueID].goals} - {player.seasonData[leagueID].assists} - {player.seasonData[leagueID].yellowCards} - {player.seasonData[leagueID].redCards} - {player.seasonData[leagueID].cleanSheets}")
    ui = option_menu(["View player in list", "Sort by goals", "Sort by assists", "Sort by goal contributions", "Sort by yellow cards", "Sort by red cards", "Sort by clean sheets"], True)
    if ui == 1:
        tempDict = {}
        for player in players_to_show:
            tempDict[player.getID()] = player
        players_to_show = tempDict
        playerID, player = search(players_to_show)
        view_player_menu(playerID, player, game)
    elif ui == 2:
        league_player_stats_menu(leagueID, league, game, sort="goals")
    elif ui == 3:
        league_player_stats_menu(leagueID, league, game, sort="assists")
    elif ui == 4:
        league_player_stats_menu(leagueID, league, game, sort="goalContributions")
    elif ui == 5:
        league_player_stats_menu(leagueID, league, game, sort="yellowCards")
    elif ui == 6:
        league_player_stats_menu(leagueID, league, game, sort="redCards")
    elif ui == 7:
        league_player_stats_menu(leagueID, league, game, sort="cleanSheets")
    elif ui == 8:
        view_league_menu(leagueID, league, game, sort="points")







def league_sort_menu(game, leagueID, league, sort):
    print(seperator())
    print(f"️🛡️️ {league.getName()} - Sort Menu")
    ui = option_menu(["Sort by Points", "Sort by matches played", "Sort by goal difference", "Sort by Goals scored", "Sort by goals conceded",
                      "Sort by total clean sheets", "Sort by average possession", "Sort by passes per 90",
                      "Sort by shots per 90", "Sort by big chances per 90", "Sort by total XG", "Sort by XG per 90", "Sort by fouls per 90", "Sort by yellow cards per 90",
                      "Sort by red cards per 90"], True)
    sort_options = {
        1: "points",
        2: "gamesPlayed",
        3: "goalDifference",
        4: "goalsScored",
        5: "goalsConceded",
        6: "cleanSheets",
        7: "averagePossession",
        8: "passesPer90",
        9: "shotsPer90",
        10: "bigChancesPer90",
        11: "xgTotal",
        12: "xgPer90",
        13: "foulsPer90",
        14: "yellowCardsPer90",
        15: "redCardsPer90",
        16: sort
    }

    sort = sort_options.get(ui, sort)
    return sort

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

    leagues = game.getLeagues()
    league = leagues[clubs[player.getClub()].getLeague()]


    print(seperator())
    print(f"️‍⛹️‍♂️ {player.getName()} | Age: {player.getAge(dateObject)} ({player.getBirthday()}) | {nations[player.getNationality()].getName()}")
    print(f"{player.getPosition().getName()} | {clubs[player.getClub()].getFullName()} {clubs[player.getClub()].printColors()} | {player.calculateRating()} | Rating: {player.calculateStarRating(playersListForStarRating)}")
    print(seperator())
    (passing, dribbling, finishing, defending, ball_control, delivery, vision, football_iq, positioning, composure, decision_making, work_rate, aggression,
     pace, strength, stamina, aerial, shot_stopping, handling, distribution, command)= player.getAttributes()

    print(f"💚 Condition: {round(player.condition)}%")
    if player.isInjured:
        injuryObject = player.getInjuryObject()
        fixture = injuryObject.getFixtureSustainedIn()
        homeTeam, awayTeam = fixture.getTeams()
        day, month, year = fixture.getDate()
        print(f"🚑 Injury Status: {injuryObject.getName()}. Sustained in {homeTeam.getName()} vs {awayTeam.getName()} on {day}/{month}/{year}.")
        if injuryObject.min_days > injuryObject.timeElapsed:
            print(f"Will be out for between {injuryObject.min_days - injuryObject.timeElapsed} and {injuryObject.max_days - injuryObject.timeElapsed} days.")
        else:
            print(f"Will be out for {injuryObject.length - injuryObject.timeElapsed} days.")
    else:
        print("🚑 Injury Status: None")

    if len(player.seasonData) != 0:

        print("")
        print("📋 Player Season Stats:")
        print("")

        for leagueID, league in player.seasonData.items():
            print(f"{leagues[leagueID].getName()}")
            print(f"🎽 {league.appearances}({league.subAppearances}) | ⚽ {league.goals} | 🥾 {league.assists} | 🟨 {league.yellowCards} | 🟥 {league.redCards}")
            print("")

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
    formation, starting_eleven, bench, playingStyle = club.getTeamSheet()

    if formation is not None and len(starting_eleven) > 0 and len(bench) > 0:
        for index, position in enumerate(formation):
            print(f"{starting_eleven[index].calculateStarRating(players)} | {positions[position].getAbbreviation()} | {starting_eleven[index].getName()}")
        for index, player in enumerate(bench):
            print(f"{player.calculateStarRating(players)} | Bench | {player.getName()}")


    ui = option_menu(["Auto Pick Team", "Set Formation", "Clear Team Sheet"], go_back_allowed=True)
    if ui == 1:
        formation, starting_eleven, bench, playingStyle = club.autoPickTeam()
        club.setTeamSheet(formation, starting_eleven, bench, playingStyle)
        team_sheet_menu(clubID, club, game)
    elif ui == 2:
        print("")
    elif ui == 3:
        formation = None
        starting_eleven = []
        bench = []
        club.setTeamSheet(formation, starting_eleven, bench, playingStyle)
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
    ui = option_menu(["⛹️‍♂️ Players", "🛡️ Clubs", "📜 Leagues", "🆚 Fixtures", "🧑‍💼 Managers", "🏟 Stadiums"], go_back_allowed=True)
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
        clubs = game.getClubs()
        fixtures = []
        for club in clubs.values():
            clubFixtures = club.getFixtures()
            for clubFixture in clubFixtures:
                if clubFixture not in fixtures:
                    fixtures.append(clubFixture)

        fixture = fixture_search(fixtures, game)
        view_fixture_menu(fixture, game)
    elif ui == 5:
        managers = game.getManagers()
        managerID, manager = search(managers)
        view_manager_menu(managerID, manager, game)
    elif ui == 6:
        stadiums = game.getStadiums()
        stadiumID, stadium = search(stadiums)
        view_stadium_menu(stadiumID, stadium, game)
    elif ui == 7:
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



