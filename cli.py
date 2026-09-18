

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
                if fixture.isCompleted is False:
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
        "1": "1️⃣",
        "2": "2️⃣",
        "3": "3️⃣",
        "4": "4️⃣",
        "5": "5️⃣",
        "6": "6️⃣",
        "7": "7️⃣",
        "8": "8️⃣",
        "9": "9️⃣",
        "0": "0️⃣"
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

        char_list = []
        for character in str(id):
            char_list.append(number_emoji_mapping[character])
        result = ''.join(char_list)

        print(f"{result} {item}")

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


def view_stadium_menu(stadiumID, game):
    clubs = game.getClubs()
    stadiums =  game.getStadiums()
    stadium = stadiums[stadiumID]

    print(seperator())
    print(f"️🏟️ {stadium.getName()}")
    print(seperator())
    print(f"📅 Opened: {stadium.getOpenedDate()}")
    print(f"👥 Capacity: {stadium.getCapacity()}")
    print(f"📍 City: {stadium.getCity()}")
    print(f"🛡️ Club: {clubs[stadium.getClubID()].getShortName()}")
    ui = option_menu([f"View {clubs[stadium.getClubID()].getShortName()}"], go_back_allowed = True)
    if ui == 1:
        clubID = stadium.getClubID()
        view_club_menu(clubID, game)
    elif ui == 2:
        return

def view_fixture_menu(fixture, game):
    homeTeam, awayTeam = fixture.getTeams()

    events = fixture.getMatchEvents()
    matchStatistics = fixture.getMatchStatistics()

    print(seperator())
    day, month, year = fixture.getDate()
    print(f"📅 {day}/{month}/{year}")
    print(f"🏟️ {game.getStadiums()[fixture.getStadiumID()].getName()}")

    if fixture.leagueID is not None:
        print(f"🏆 {game.getLeagues()[fixture.getLeagueID()].getName()}")
    elif fixture.tournamentID is not None:
        print(f"🏆 {game.tournaments[fixture.getTournamentID()].getName()} - {fixture.getStage()}")

    if fixture.isCompleted:
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
        view_club_menu(homeTeam.getID(), game)
    elif ui == 2:
        view_club_menu(awayTeam.getID(), game)
    elif ui == 3:
        return



def view_manager_menu(managerID, game):

    nations = game.getNations()
    managers = game.getManagers()
    clubs = game.getClubs()
    manager = managers[managerID]

    print(seperator())
    print(f"️🧑‍💼 {manager.getName()} | {clubs[manager.getClubID()].getFullName()}")
    print(seperator())
    print(f"Age: {manager.getAge()}")
    print(f"Nationality: {nations[manager.getNationID()].getName()}")
    ui = option_menu([f"View {clubs[manager.getClubID()].getShortName()}"], go_back_allowed = True)
    if ui == 1:
        clubID = manager.getClubID()
        view_club_menu(clubID, game)
    elif ui == 2:
        return

def view_free_agents_menu(clubID, game):
    clubs = game.getClubs()
    club = clubs[clubID]
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


def view_club_fixtures(clubID, game):

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
    clubs = game.getClubs()
    club = clubs[clubID]

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

        if fixture.getLeagueID() is not None:
            league = leagues[fixture.getLeagueID()]
        else:
            tournaments = game.getTournaments()
            league = tournaments[fixture.getTournamentID()]


        if fixture.isCompleted:
            hScore, aScore = fixture.getScore()

        if fixture.isCompleted and fixture.getType() == "league":
            print(f"{league.getName()} | {day}/{month}/{year} | {home.getShortName()} {hScore} - {away.getShortName()} {aScore}")
        elif fixture.isCompleted and fixture.getType() == "knockout":
            print(f"{league.getName()} | {fixture.getStage()} | {day}/{month}/{year} | {home.getShortName()} {hScore} - {away.getShortName()} {aScore}")
        elif fixture.isCompleted is False and fixture.getType() == "league":
            print(f"{league.getName()} | {day}/{month}/{year} | {home.getShortName()} - {away.getShortName()}")
        elif fixture.isCompleted is False and fixture.getType() == "knockout":
            print(f"{league.getName()} | {fixture.getStage()} | {day}/{month}/{year} | {home.getShortName()} - {away.getShortName()}")

    ui = option_menu([f"View {club.getFullName()}", "View a fixture"], go_back_allowed=True)
    if ui == 1:
        view_club_menu(clubID, game)
    elif ui == 2:
        clubFixtures = club.getFixtures()
        for clubFixture in clubFixtures:
            if clubFixture not in fixtures:
                fixtures.append(clubFixture)

        fixture = fixture_search(fixtures, game)
        view_fixture_menu(fixture, game)
    elif ui == 3:
        return

def view_league_menu(leagueID, game, sort="points", year="current"):

    if year == "current":
        year = game.currentSeason

    tempYear = year
    tempPrevYear = str(tempYear - 1)
    tempYear = str(tempYear)
    label = f"{tempPrevYear[-2:]}/{tempYear[-2:]}"

    nations = game.getNations()
    leagues = game.getLeagues()
    league = leagues[leagueID]

    nationObject = nations[league.getNationID()]

    print(seperator())
    print(f"🛡️ {league.getName()} - {nationObject.getName()} - {label}")
    print(seperator())

    clubList = []
    if year == game.currentSeason:
        clubList = list(league.getClubs().values())
        year = "current"
    else:
        for club in game.getClubs().values():
            if club.getID() != 0:
                if leagueID in club.seasonHistory[year].keys():
                    clubList.append(club)

    sort_functions = {
        "points": (lambda c: (-c.getSeasonData(leagueID, year).getPoints(), -c.getSeasonData(leagueID, year).getGoalDifference(), -c.getSeasonData(leagueID, year).goalsFor, c.getFullName()), "Normal"),
        "gamesPlayed": (lambda c: c.getSeasonData(leagueID, year).matchesPlayed, "Normal"),
        "goalDifference": (lambda c: c.getSeasonData(leagueID, year).getGoalDifference(), "Normal"),
        "goalsScored": (lambda c: c.getSeasonData(leagueID, year).goalsFor, "Data"),
        "goalsConceded": (lambda c: c.getSeasonData(leagueID, year).goalsAgainst, "Data"),
        "cleanSheets": (lambda c: c.getSeasonData(leagueID, year).cleanSheets, "Data"),
        "averagePossession": (lambda c: safe_divide(c.getSeasonData(leagueID, year).totalPossession, c.getSeasonData(leagueID, year).matchesPlayed), "Data"),
        "passesPer90": (lambda c: safe_divide(c.getSeasonData(leagueID, year).totalPasses, c.getSeasonData(leagueID, year).matchesPlayed), "Data"),
        "shotsPer90": (lambda c: safe_divide(c.getSeasonData(leagueID, year).totalShots, c.getSeasonData(leagueID, year).matchesPlayed), "Data"),
        "bigChancesPer90": (lambda c: safe_divide(c.getSeasonData(leagueID, year).totalBigChances, c.getSeasonData(leagueID, year).matchesPlayed), "Data"),
        "xgTotal": (lambda c: c.getSeasonData(leagueID, year).totalXG, "Data"),
        "xgPer90": (lambda c: safe_divide(c.getSeasonData(leagueID, year).totalXG, c.getSeasonData(leagueID, year).matchesPlayed), "Data"),
        "fouls": (lambda c: c.getSeasonData(leagueID, year).totalFouls, "Data"),
        "yellowCards": (lambda c: c.getSeasonData(leagueID, year).totalYellowCards, "Data"),
        "redCards": (lambda c: c.getSeasonData(leagueID, year).totalRedCards, "Data"),
        "mediaPrediction": (lambda c: c.calculateBettingOdds(game), "Media Prediction")
    }

    sort_key, view = sort_functions[sort]

    clubList.sort(
        key=sort_key,
        reverse=(sort != "points" and sort != "mediaPrediction")
    )

    if view == "Normal":

        print("Pos | Club | Pl | W | D | L | GD | Pts")
        print(seperator())

        for pos, club in enumerate(clubList, start=1):

            sd = club.getSeasonData(leagueID, year)

            print(
                f"{pos}. {club.getFullName()} - "
                f"{sd.matchesPlayed} Pl - "
                f"{sd.wins} W - "
                f"{sd.draws} D - "
                f"{sd.losses} L - "
                f"{sd.getGoalDifference()} GD - "
                f"{sd.getPoints()} Pts"
            )

    elif view == "Media Prediction":

        print("Pos | Club | Odds")
        print(seperator())

        for pos, club in enumerate(clubList, start=1):
            print(
                f"{pos}. {club.getFullName()} - "
                f"{club.calculateBettingOdds(game)}/1"
            )

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
            "fouls": "Fouls",
            "yellowCards": "Yellow Cards",
            "redCards": "Red Cards",
        }

        print(f"Pos | Club | {headers[sort]}")
        print(seperator())

        value_functions = {
            "goalsScored": lambda c: c.getSeasonData(leagueID, year).goalsFor,
            "goalsConceded": lambda c: c.getSeasonData(leagueID, year).goalsAgainst,
            "cleanSheets": lambda c: c.getSeasonData(leagueID, year).cleanSheets,
            "averagePossession": lambda c: f"{safe_divide(c.getSeasonData(leagueID, year).totalPossession, c.getSeasonData(leagueID, year).matchesPlayed):.1f}%",
            "passesPer90": lambda c: f"{safe_divide(c.getSeasonData(leagueID, year).totalPasses, c.getSeasonData(leagueID, year).matchesPlayed):.1f}",
            "shotsPer90": lambda c: f"{safe_divide(c.getSeasonData(leagueID, year).totalShots, c.getSeasonData(leagueID, year).matchesPlayed):.1f}",
            "bigChancesPer90": lambda c: f"{safe_divide(c.getSeasonData(leagueID, year).totalBigChances, c.getSeasonData(leagueID, year).matchesPlayed):.1f}",
            "xgTotal": lambda c: f"{c.getSeasonData(leagueID, year).totalXG:.1f}",
            "xgPer90": lambda c: f"{safe_divide(c.getSeasonData(leagueID, year).totalXG, c.getSeasonData(leagueID, year).matchesPlayed):.2f}",
            "fouls": lambda c: c.getSeasonData(leagueID, year).totalFouls,
            "yellowCards": lambda c: c.getSeasonData(leagueID, year).totalYellowCards,
            "redCards": lambda c: c.getSeasonData(leagueID, year).totalRedCards,
        }

        get_value = value_functions[sort]

        for pos, club in enumerate(clubList, start=1):
            print(f"{pos}. {club.getFullName()} - {get_value(club)}")

    ui = option_menu(["View club in league","Sort Menu","View player stats","View Media Prediction", "Next Season", "Previous Season"],True)


    if ui == 1:
        clubDict = {club.getID(): club for club in clubList}
        clubID, club = search(clubDict)
        view_club_menu(clubID, game)

    elif ui == 2:
        modifiedSort = league_sort_menu(game, leagueID, sort)
        view_league_menu(leagueID, game, modifiedSort, year)

    elif ui == 3:
        league_player_stats_menu(leagueID, game, year, sort="goals")

    elif ui == 4:
        view_league_menu(leagueID, game, "mediaPrediction", year)

    elif ui == 5:
        if year == "current":
            year = game.currentSeason

        if (year + 1) <= game.currentSeason:
            year = year + 1

        view_league_menu(leagueID, game, "points", year)

    elif ui == 6:
        if year == "current":
            year = game.currentSeason

        if (year - 1) >= game.startingSeason:
            year = year - 1

        view_league_menu(leagueID, game, "points", year)

    elif ui == 7:
        return




def league_player_stats_menu(leagueID, game, year, sort="goals"):

    players = game.getPlayers()
    leagues = game.getLeagues()
    league = leagues[leagueID]
    positions = game.getPositions()

    print(seperator())
    print(f"🛡️ {league.getName()}")
    print(seperator())
    players_in_league = []
    for player in players.values():
        if year == "current":
            for playerLeagueID in player.seasonData.keys():
                if playerLeagueID == leagueID:
                    players_in_league.append(player)
        else:
            if year in player.seasonHistory.keys():
                for playerLeagueID in player.seasonHistory[year].keys():
                    if playerLeagueID == leagueID:
                        players_in_league.append(player)

    if sort == "goals":
        players_in_league.sort(key=lambda p: p.getSeasonData(leagueID, year).goals, reverse=True)
    elif sort == "assists":
        players_in_league.sort(key=lambda p: p.getSeasonData(leagueID, year).assists, reverse=True)
    elif sort == "goalContributions":
        players_in_league.sort(key=lambda p: p.getSeasonData(leagueID, year).goals + p.getSeasonData(leagueID, year).assists, reverse=True)
    elif sort == "yellowCards":
        players_in_league.sort(key=lambda p: p.getSeasonData(leagueID, year).yellowCards, reverse=True)
    elif sort == "redCards":
        players_in_league.sort(key=lambda p: p.getSeasonData(leagueID, year).redCards, reverse=True)
    elif sort == "cleanSheets":
        players_in_league.sort(key=lambda p: p.getSeasonData(leagueID, year).cleanSheets, reverse=True)

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
        print(f"{player.getName()} - {positions[player.getPositionID()].getAbbreviation()} - {player.getSeasonData(leagueID, year).goals} - {player.getSeasonData(leagueID, year).assists} - {player.getSeasonData(leagueID, year).yellowCards} - {player.getSeasonData(leagueID, year).redCards} - {player.getSeasonData(leagueID, year).cleanSheets}")
    ui = option_menu(["View player in list", "Sort by goals", "Sort by assists", "Sort by goal contributions", "Sort by yellow cards", "Sort by red cards", "Sort by clean sheets"], True)
    if ui == 1:
        tempDict = {}
        for player in players_to_show:
            tempDict[player.getID()] = player
        players_to_show = tempDict
        playerID, player = search(players_to_show)
        view_player_menu(playerID, game)
    elif ui == 2:
        league_player_stats_menu(leagueID, game, year, sort="goals")
    elif ui == 3:
        league_player_stats_menu(leagueID, game, year, sort="assists")
    elif ui == 4:
        league_player_stats_menu(leagueID, game, year, sort="goalContributions")
    elif ui == 5:
        league_player_stats_menu(leagueID, game, year, sort="yellowCards")
    elif ui == 6:
        league_player_stats_menu(leagueID, game, year, sort="redCards")
    elif ui == 7:
        league_player_stats_menu(leagueID, game, year, sort="cleanSheets")
    elif ui == 8:
        view_league_menu(leagueID, game, sort="points", year=year)



def season_data_search_menu(game):
    cDay, cMonth, cYear = game.getDateObject().getDate()
    playerManagerClub = game.getClubs()[game.managers[game.playerManagerID].getClubID()]

    passed = False
    ui = option_menu(["View Current Season", "View Older Season"], go_back_allowed=True)
    if ui == 1:
        return "current"
    elif ui == 2:
        while not passed:
            ui = user_input("integer","Please enter the last year of the season you wish to look at: e.g 2018/19 -> 2019")
            if ui > cYear or ui not in list(playerManagerClub.seasonHistory.keys()):
                print("No completed season data exists for that year!")
            elif ui == cYear:
                return "current"
            else:
                return ui
    elif ui == 3:
        return "current"



def league_sort_menu(game, leagueID, sort):
    leagues = game.getLeagues()
    league = leagues[leagueID]

    print(seperator())
    print(f"️🛡️️ {league.getName()} - Sort Menu")
    ui = option_menu(["Sort by Points", "Sort by matches played", "Sort by goal difference", "Sort by Goals scored", "Sort by goals conceded",
                      "Sort by total clean sheets", "Sort by average possession", "Sort by passes per 90",
                      "Sort by shots per 90", "Sort by big chances per 90", "Sort by total XG", "Sort by XG per 90", "Sort by fouls", "Sort by yellow cards",
                      "Sort by red cards"], True)
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
        13: "fouls",
        14: "yellowCards",
        15: "redCards",
        16: sort
    }

    sort = sort_options.get(ui, sort)
    return sort

def view_club_menu(clubID, game):

    if clubID == 0:
        view_free_agents_menu(clubID, game)
        return

    leagues = game.getLeagues()
    managers = game.getManagers()
    clubs = game.getClubs()
    stadiums = game.getStadiums()
    club = clubs[clubID]

    leagueID = club.getLeagueID()
    leagueObject = leagues[leagueID]

    playerManagerID = game.playerManagerID
    playerManagerClubID = managers[playerManagerID].getClubID()


    print(seperator())
    print(f"️🛡️️ {club.getFullName()} {club.printColors()}")
    print(seperator())
    print("📖 About Club")
    print(f"Founded: {club.getFoundedDate()}")
    print(f"Nickname: {club.getNickname()}")
    print(f"Reputation: {club.getReputation()}")
    print("")
    print("📈 Club Finances")
    print(f"Transfer Budget: {club.getTransferBudget()}")
    print(f"Total Player Wages: £{club.getTotalPlayerWages()}")
    print("")
    print("🧑‍💼 Manager")
    print(f"Name: {managers[club.getManagerID()].getName()}")
    print("")
    print("🏟️ Stadium")
    print(f"Name: {stadiums[club.getStadiumID()].getName()}")

    ui = option_menu([f"View {club.getFullName()} Squad", f"View {leagueObject.getName()}", f"View {club.getShortName()}'s Fixtures", f"View {managers[club.getManagerID()].getName()}", f"View {stadiums[club.getStadiumID()].getName()}"], True)
    if ui == 1:
        if clubs[playerManagerClubID] == club:
            view_squad_screen(clubID, game, sort="position")
        else:
            page = 1
            settings = {"Club": club.id}
            player_database_menu(game, page, settings)
    elif ui == 2:
        view_league_menu(leagueID, game)
    elif ui == 3:
        view_club_fixtures(clubID, game)
    elif ui == 4:
        managerID = club.getManagerID()
        view_manager_menu(managerID, game)
    elif ui == 5:
        stadiumID = club.getStadiumID()
        view_stadium_menu(stadiumID, game)
    elif ui == 6:
        return

def player_transfer_menu(playerID, game):

    players = game.getPlayers()
    managers = game.getManagers()
    clubs = game.getClubs()

    playerManagerID = game.playerManagerID
    playerManagerObject = managers[playerManagerID]
    playerManagerClubID = managers[playerManagerID].getClubID()

    player = players[playerID]

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
            view_player_menu(playerID, game)
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
            player_transfer_menu(playerID, game)
        elif ui == 3:
            view_player_menu(playerID, game)


def view_player_history_menu(playerID, game, year="current"):

    players = game.getPlayers()
    player = players[playerID]
    clubs = game.getClubs()
    leagues = game.getLeagues()
    tournaments = game.getTournaments()

    if year == "current":
        seasonData = player.seasonData
        displayYear = game.currentSeason
    else:
        seasonData = player.seasonHistory[year]
        displayYear = year

    print(seperator())

    year = displayYear
    prevYear = str(year - 1)
    yearStr = str(year)
    label = f"{prevYear[-2:]}/{yearStr[-2:]}"

    print(f"📜 {player.getName()} | Season History | {label}")
    print(seperator())

    # GROUPS COMPETITIONS BY CLUB
    clubGrouping = {}
    for tournamentID, data in seasonData.items():
        clubID = data.clubID
        if clubID not in clubGrouping:
            clubGrouping[clubID] = []
        clubGrouping[clubID].append(tournamentID)

    if len(clubGrouping) == 0:
        print("⚠️ No data recorded for this season!")
    else:
        for clubID in clubGrouping:
            print(f"🛡️ {clubs[clubID].getName()}")
            for tournamentID in clubGrouping[clubID]:
                data = seasonData[tournamentID]
                if tournamentID in leagues:
                    name = leagues[tournamentID].getName()
                elif tournamentID in tournaments:
                    name = tournaments[tournamentID].getName()
                print(f" 🏆 {name}")
                print(f"    🎽 Appearances: {data.appearances} ({data.subAppearances})")
                print(f"    ⚽ Goals: {data.goals}")
                print(f"    🥾 Assists: {data.assists}")
                print(f"    🟨 Yellow: {data.yellowCards}")
                print(f"    🟥 Red: {data.redCards}")
                print(f"    🧤 Clean Sheets: {data.cleanSheets}")


    if year == "current":
        numericYear = game.currentSeason
    else:
        numericYear = year

    ui = option_menu(["Next Season", "Previous Season"], go_back_allowed=True)

    if ui == 1:
        if year == "current":
            view_player_history_menu(playerID, game, "current")
        elif (numericYear + 1) >= game.currentSeason:
            view_player_history_menu(playerID, game, "current")
        else:
            view_player_history_menu(playerID, game, numericYear + 1)

    elif ui == 2:
        previousYear = numericYear - 1
        if previousYear >= game.startingSeason and previousYear in player.seasonHistory.keys():
            view_player_history_menu(playerID, game, previousYear)
        else:
            view_player_history_menu(playerID, game, year)

    elif ui == 3:
        view_player_menu(playerID, game)

def view_player_menu(playerID, game):

    players = game.getPlayers()
    player = players[playerID]

    clubs = game.getClubs()
    positions = game.getPositions()
    managers = game.getManagers()
    nations = game.getNations()
    leagues = game.getLeagues()
    tournaments = game.getTournaments()
    dateObject = game.getDateObject()

    playerManagerID = game.playerManagerID
    playerManagerClubID = managers[playerManagerID].getClubID()
    if playerManagerClubID != 0:
        playersListForStarRating = clubs[playerManagerClubID].getFirstTeam()
    else:
        playersListForStarRating = players


    print(seperator())
    print(f"️‍⛹️‍♂️ {player.getName()} | Age: {player.getAge(dateObject)} ({player.getBirthday()}) | {nations[player.getNationID()].getName()}")
    print(f"{positions[player.getPositionID()].getName()} | {clubs[player.getClubID()].getFullName()} {clubs[player.getClubID()].printColors()} | {player.calculateRating()} | Rating: {player.calculateStarRating(playersListForStarRating)}")
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

            if leagueID in leagues.keys():
                print(f"{leagues[leagueID].getName()}")
            elif leagueID in tournaments.keys():
                print(f"{tournaments[leagueID].getName()}")
            print(f"🎽 {league.appearances}({league.subAppearances}) | ⚽ {league.goals} | 🥾 {league.assists} | 🟨 {league.yellowCards} | 🟥 {league.redCards}")
            print("")

    print("📊 Attributes:")
    if player.getPositionID() == 1:
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

    if player.getClubID() != 0:
        print("")
        print("🛡️ Club:")
        print(f"Club: {clubs[player.getClubID()].getFullName()}")
        print(f"Wage: £{player.getCurrentWage()} per week")
        print(f"Contract Length: {player.getContractLength()} years remaining")

    ui = option_menu([f"View {clubs[player.getClubID()].getFullName()}", "Transfer Options", "View Player Season History"], go_back_allowed = True)
    if ui == 1:
        view_club_menu(player.getClubID(), game)
    elif ui == 2:
        player_transfer_menu(playerID, game)
    elif ui == 3:
        view_player_history_menu(playerID, game)
    elif ui == 4:
        return


def database_view_settings_menu(game, settings):
    clubs = game.getClubs()
    leagues = game.getLeagues()
    print(seperator())
    print(f"Player Database View Filters Menu")
    if len(settings) != 0:
        print(seperator())
        for key, setting in settings.items():
            print(f"{key}: {setting}")
    ui = option_menu(["Add Age Restriction", "Free Agents Only", "Club", "League", "Clear All"], go_back_allowed = True)
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
        settings["Club"] = club.id
        return settings
    elif ui == 4:
        leagueID, league = search(leagues)
        settings["League"] = league.id
        return settings
    elif ui == 5:
        settings = {}
        return settings
    elif ui == 6:
        return settings

def player_database_menu(game, page = 1, settings = None):

    if settings is None:
        settings = {}

    dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()

    playerManagerID = game.playerManagerID
    playerManagerObject = managers[playerManagerID]
    playerManagerClubID = managers[playerManagerID].getClubID()
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
            if player.getClubID() != 0:
                players_to_remove.append(player)
    if "Player Shortlist" in settings.keys():
        for player in playerList:
            if player not in playerManagerObject.getShortlist():
                players_to_remove.append(player)
    if "Club" in settings.keys():
        for player in playerList:
            if player.getClubID() != settings["Club"]:
                players_to_remove.append(player)
    elif "League" in settings.keys():
        for player in playerList:
            if clubs[player.getClubID()].getLeagueID() != settings["League"]:
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
              f"| {positions[player.getPositionID()]} | {clubs[player.getClubID()].getShortName()} | {nations[player.getNationID()].getAbbreviation()} | {player.getAge(dateObject)} | {player.getName()} | {player.calculateRating()} | {player.potential}")

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
        view_player_menu(playerID, game)
    elif ui == 4:
        settings = database_view_settings_menu(game, settings)
        player_database_menu(game, page, settings)
    elif ui == 5:
        recruitment_menu(game)


def staff_database_menu(game, page = 1, settings = None):

    if settings is None:
        settings = {}

    managers = game.getManagers()
    nations = game.getNations()
    clubs = game.getClubs()

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
        print(f"{clubs[staff.getClubID()].getShortName()} | {nations[staff.getNationID()].getAbbreviation()} | {staff.getAge()} | {staff.getName()}")

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
        view_manager_menu(managerID, game)
    elif ui == 4:
        recruitment_menu(game)

def team_sheet_menu(clubID, game):
    clubs = game.getClubs()
    club = clubs[clubID]
    positions = game.getPositions()
    first_team = club.getFirstTeam()

    formation, starting_eleven, bench, playingStyle = club.getTeamSheet()

    print(seperator())
    print(f"{clubs[clubID].printColors()} {clubs[clubID].getFullName()}'s Team Sheet")
    print(f"Style - {playingStyle}")
    print(seperator())

    if formation is not None and len(starting_eleven) > 0 and len(bench) > 0:
        print("Pos | Star Rating in Position | Best Pos | Name")
        print(seperator())
        for index, position in enumerate(formation):
            if starting_eleven[index] is not None:
                print(f"{positions[position].getAbbreviation()} | {starting_eleven[index].calculateStarRating(first_team, position)} | "
                      f"{positions[starting_eleven[index].getPositionID()].getAbbreviation()} | {starting_eleven[index].getName()}")
            else:
                print(f"{positions[position].getAbbreviation()} | None selected")

        for index, player in enumerate(bench):
            if bench[index] is not None:
                print(f"Bench {index+1} | {player.calculateStarRating(first_team)} | {positions[player.getPositionID()].getAbbreviation()} | {player.getName()}")
            else:
                print(f"Bench {index+1} | None Selected")


    ui = option_menu(["Auto Pick Team", "Set Formation", "Set Playing Style", "Add / Replace Player", "Clear Team Sheet"], go_back_allowed=True)
    if ui == 1:
        formation, starting_eleven, bench, playingStyle = club.autoPickTeam(game)
        club.setTeamSheet(formation, starting_eleven, bench, playingStyle)
        team_sheet_menu(clubID, game)
    elif ui == 2:
        formation = formation_selector_menu(clubID, game)

        starting_eleven = []
        for i in range(11):
            starting_eleven.append(None)
        bench = []
        for i in range(7):
            bench.append(None)
        club.setTeamSheet(formation, starting_eleven, bench, playingStyle)
        team_sheet_menu(clubID, game)
    elif ui == 3:
        playingStyle = playstyle_selector_menu(clubID, game)
        club.setTeamSheet(formation, starting_eleven, bench, playingStyle)
        team_sheet_menu(clubID, game)
    elif ui == 4:
        if formation is None:
           print("⚠️ Please select a formation first!")
           team_sheet_menu(clubID, game)
        else:
            replace_player_menu(clubID, game)
    elif ui == 5:
        formation = None
        starting_eleven = []
        bench = []
        club.setTeamSheet(formation, starting_eleven, bench, playingStyle)
        team_sheet_menu(clubID, game)
    elif ui == 6:
        return


def formation_selector_menu(clubID, game):
    clubs = game.getClubs()
    club = clubs[clubID]
    formations = club.FORMATIONS

    options = []
    for formation in formations.keys():
        options.append(formation)

    ui = option_menu(options, go_back_allowed=True)

    if ui == len(options) + 1:
        return
    else:
        formationSelected = options[ui - 1]
        formation = formations[formationSelected]
        return formation


def playstyle_selector_menu(clubID, game):
    clubs = game.getClubs()
    club = clubs[clubID]
    playing_styles = club.PLAYING_STYLES

    ui = option_menu(playing_styles, go_back_allowed=True)
    if ui == len(playing_styles) + 1:
        return
    else:
        styleSelected = playing_styles[ui - 1]
        return styleSelected


def replace_player_menu(clubID, game):
    clubs = game.getClubs()
    club = clubs[clubID]
    players = club.first_team
    positions = game.getPositions()

    ui = option_menu(["Starting XI", "Bench"], go_back_allowed=True, customText="Would you like to make a change to the starting XI or bench?")
    if ui == 1:
        selected = "startingXI"
    elif ui == 2:
        selected = "bench"
    elif ui == 3:
        team_sheet_menu(clubID, game)
        return

    if selected == "startingXI":
        options = []
        for position in club.formation:
            options.append(positions[position].getAbbreviation())
        ui = option_menu(options, go_back_allowed=False)
        selectedPositionIndex = ui - 1
        selectedPosition = club.formation[selectedPositionIndex]

        candidates = []
        for player in club.first_team:
            if player.positionID == selectedPosition or player.canPlayPosition(selectedPosition):
                candidates.append(player)
        candidates.sort(key=lambda player: player.calculateRating(), reverse=True)
        options = []
        print("Name | Star Rating in Position | Preferred Position | Current Position")
        for player in candidates:

            additional_detail = ""
            if player in club.starting_eleven:
                position = club.formation[club.starting_eleven.index(player)]
                additional_detail = f"| Player selected in Starting Eleven at {position}"
            elif player in club.bench:
                position = club.formation[club.bench.index(player)]
                additional_detail = f"| Player selected in Bench at {position}"

            options.append(f"{player.getName()} | {player.calculateStarRating(players, selectedPosition)} | {positions[player.getPositionID()].getAbbreviation()} {additional_detail}")

        ui = option_menu(options, go_back_allowed=False)
        selectedPlayer = candidates[ui - 1]

        if selectedPlayer in club.starting_eleven:
            positionIndex = club.starting_eleven.index(selectedPlayer)
            club.starting_eleven[positionIndex] = None

        if selectedPlayer in club.bench:
            positionIndex = club.bench.index(selectedPlayer)
            club.bench[positionIndex] = None

        club.starting_eleven[selectedPositionIndex] = selectedPlayer

    elif selected == "bench":
        options = []
        for index, position in enumerate(club.bench):
            options.append(f"Bench Slot {index+1}")
        ui = option_menu(options, go_back_allowed=False)
        selectedPositionIndex = ui - 1
        selectedPosition = club.formation[selectedPositionIndex]

        candidates = []
        for player in club.first_team:
            candidates.append(player)
        options = []
        print("Name | Star Rating in Position | Preferred Position")
        for player in candidates:

            additional_detail = ""
            if player in club.starting_eleven:
                position = club.formation[club.starting_eleven.index(player)]
                additional_detail = f"| Player selected in Starting Eleven at {position}"
            elif player in club.bench:
                position = club.formation[club.bench.index(player)]
                additional_detail = f"| Player selected in Bench at {position}"

            options.append(
                f"{player.getName()} | {player.calculateStarRating(players, selectedPosition)} | {positions[player.getPositionID()].getAbbreviation()} {additional_detail}")
        ui = option_menu(options, go_back_allowed=False)
        selectedPlayer = candidates[ui - 1]

        if selectedPlayer in club.starting_eleven:
            positionIndex = club.starting_eleven.index(selectedPlayer)
            club.starting_eleven[positionIndex] = None

        if selectedPlayer in club.bench:
            positionIndex = club.bench.index(selectedPlayer)
            club.bench[positionIndex] = None

        club.bench[selectedPositionIndex] = selectedPlayer

    team_sheet_menu(clubID, game)



def view_squad_screen(clubID, game, sort = "position", type = "firstTeam"):
    dateObject = game.getDateObject()
    nations = game.getNations()
    clubs = game.getClubs()
    positions = game.getPositions()

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
        clubPlayers.sort(key=lambda p: p.getPositionID())
    elif sort == "age":
        clubPlayers.sort(key=lambda p: p.getAge(dateObject))

    print("Star Rating | Pos | Nation | Age | Name")
    print(seperator())
    for player in clubPlayers:
        print(f"{player.calculateStarRating(firstTeam)} | {positions[player.getPositionID()].getAbbreviation()} | {nations[player.getNationID()].getAbbreviation()} | {player.getAge(dateObject)} | {player.getName()}")
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
        view_player_menu(playerID, game)
    elif ui == 7:
        return

def universal_search_menu(game):
    ui = option_menu(["⛹️‍♂️ Players", "🛡️ Clubs", "📜 Leagues", "🆚 Fixtures", "🧑‍💼 Managers", "🏟 Stadiums"], go_back_allowed=True)
    if ui == 1:
        players = game.getPlayers()
        playerID, player = search(players)
        view_player_menu(playerID, game)
    elif ui == 2:
        clubs = game.getClubs()
        clubID, club = search(clubs)
        view_club_menu(clubID, game)
    elif ui == 3:
        leagues = game.getLeagues()
        leagueID, league = search(leagues)
        view_league_menu(leagueID, game)
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
        view_manager_menu(managerID, game)
    elif ui == 6:
        stadiums = game.getStadiums()
        stadiumID, stadium = search(stadiums)
        view_stadium_menu(stadiumID, game)
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

        playerManagerID = game.playerManagerID
        playerManagerClubID = managers[playerManagerID].getClubID()
        clubObject = clubs[playerManagerClubID]

        day, month, year = dateObject.getDate()


        if len(clubObject.getFixtures()) == 0:
            next_fixture = None
        else:
            for fixture in clubObject.getFixtures():
                if fixture.isCompleted is False:
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
            team_sheet_menu(playerManagerClubID, game)
        elif ui == 3:
            view_squad_screen(playerManagerClubID, game)
        elif ui == 4:
            view_club_menu(playerManagerClubID, game)
        elif ui == 5:
            view_club_fixtures(playerManagerClubID, game)
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

def createManager(game):

    nations = game.getNations()
    clubs = game.getClubs()
    managers = game.getManagers()

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

    return firstName, lastName, age, nationID, clubID



def initial_menu():
    print("")

    ui = (option_menu(["Start a new game", "Close Game", "Test"]))
    if ui == 1:
        return "start"
    elif ui == 2:
        return "close"
    elif ui == 3:
        return "test"

