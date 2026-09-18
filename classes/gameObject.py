from read_from_file import *
import copy
from registry import get_class

from mathematical_models import rounddp

from match_engine import simulate_match
from match_engine import simulate_match_extra_time
from match_engine import simulate_penalties

from player_generation_engine import build_fake_player_database
from player_generation_engine import club_generate_fake_players
from player_generation_engine import youth_intake

from cli import team_sheet_menu

Date = get_class('Date')
Player = get_class('Player')
Injury = get_class('Injury')
Club = get_class('Club')
League = get_class('League')
Manager = get_class('Manager')
Stadium = get_class('Stadium')
Nation = get_class('Nation')
Position = get_class('Position')
freeAgents = get_class('FreeAgents')


class GameObject:
    def __init__(self):

        self.tournaments = {}

        self.onHoliday = False
        self.holidayDate = None

        self.playerManagerID = 1878
        self.databaseType = "fake"

        self.dateObject = Date()
        self.dateObject.setDate(2, 7, 2025)
        self.startingSeason = self.dateObject.year + 1
        self.currentSeason = self.startingSeason

        self.clubs = read_clubs_from_database(Club)
        self.leagues = read_leagues_from_database(League)
        self.managers = read_managers_from_database(Manager)
        self.stadiums = read_stadiums_from_database(Stadium)
        self.nations = read_nations_from_database(Nation)
        self.positions = read_positions_from_database(Position)
        self.names = read_names_from_file(self.nations)

        f = freeAgents(0, "Free Agents", "Free Agents")
        self.clubs[f.getID()] = f

        """
        If a real database is selected, it will load the players from the players.fmdata file and after initializing the players to clubs, if any clubs
        have absolutely no players, fake players will be generated.
        
        If a fake database is selected, the build_fake_player_database function will generate players for all clubs, and after each club, it will add all 
        those players to the game main players dictionary and also initialize the player to their club.
        """

        if self.databaseType == "real":
            self.players = read_players_from_file(Player)

        elif self.databaseType == "fake":
            self.players = {}
            build_fake_player_database(self)

            for club in self.clubs.values():
                if club.getID() != 0:
                    youth_intake(self, club)

        initialize_players(self.players, self.clubs)
        initialize_leagues(self.clubs, self.leagues)
        initialize_managers(self.managers, self.clubs)
        initialize_stadiums(self.stadiums, self.clubs)

        if self.databaseType == "real":
            for club in self.clubs.values():
                if club.getID() != 0:
                    if len(club.getPlayers()) < 1:
                        players = club_generate_fake_players(self, club)
                        for player in players:
                            self.players[player.getID()] = player
                            club.addPlayer(player)


        # ARRANGES ALL LEAGUE'S FIXTURES
        for league in self.leagues.values():
            tempDate = copy.deepcopy(self.getDateObject())
            league.arrangeFixtures(tempDate)

        # SPLITS CLUB PLAYERS INTO FIRST TEAM AND YOUTH ACADEMY

        for club in self.clubs.values():
            if club.getID() != 0:
                club.autoSplitPlayers(self)

    def getAll(self):
        return self.dateObject, self.players, self.positions, self.clubs, self.leagues, self.managers, self.stadiums, self.nations


    def annualUpdate(self):
        for player in self.players.values():
            # REMOVING LOANS
            if player.getParentClubID() != player.getClubID():

                parentClubObject = self.clubs[player.getParentClubID()]
                loanClubObject = self.clubs[player.getLoanClubID()]

                player.setClubID(player.getParentClubID())
                if player in loanClubObject.getPlayers():
                    # Removes player from loan club
                    loanClubObject.getPlayers().remove(player)
                    # Adds them back to parent club roster
                    parentClubObject.getPlayers().append(player)

                player.setLoanClubID(None)

            # PLAYER CONTRACT LENGTH DECREASE
            if player.getContractLength() > 0:
                player.decrementContractLength()

            # HANDLING CONTRACT EXPIRY PLAYERS
            if player.getContractLength() == 0:
                clubObject = self.clubs[player.getClubID()]
                if player in clubObject.getPlayers():
                    # Removes player from club
                    clubObject.getPlayers().remove(player)

                # Adds player to Free Agents
                player.setClubID(0)
                player.setParentClubID(0)
                player.setLoanClubID(None)
                self.clubs[0].getPlayers().append(player)

        for manager in self.managers.values():
            # INCREMENTING PLAYER AGES BY 1
            manager.incrementAge()

        # SPLITS CLUB PLAYERS INTO FIRST TEAM AND YOUTH ACADEMY

        for club in self.clubs.values():
            if club.getID() != 0:
                club.autoSplitPlayers(self)

    def seasonUpdate(self):

        """
        CLUB REPUTATION MODIFICATION

        1 - For every league in the game, the median value (often 12, e.g. in the EFL and is 10 in the Prem), and a list of its clubs are generated.
        2 - For every club, it will find its position in the league
        3 - Finds the club's 'Target' reputation - this is calculated by using a linear equation setting the max target at ~ 20 points above the league's reputation
        (for winning league) and min target 20 points below (for finishing rock bottom) in a league of 12 teams.
        4 - Finds difference between the target value and club current reputation, and adds half the difference to the club's reputation - creates effect where the club
        will 'close in' on the reputation for the place they have finished in, if they were to finish there for a number of consecutive seasons.
        """
        for league in self.leagues.values():

            leagueTeamCount = len(league.getClubs())
            leagueMedian = rounddp(leagueTeamCount / 2,0)
            clubs = league.getClubs()
            clubList = []
            for club in clubs.values():
                clubList.append(club)
            clubList.sort(key=lambda club: (-club.getSeasonData(league.getLeagueID()).getPoints(),
                                            -club.getSeasonData(league.getLeagueID()).getGoalDifference(),
                                            -club.getSeasonData(league.getLeagueID()).goalsFor, club.getFullName()))


            for club in league.getClubs().values():

                for index, traversedClub in enumerate(clubList):
                    if club == traversedClub:
                        break
                clubLeaguePosition = index + 1

                if club.getID() != 0:
                    targetValue = (5/3) * (leagueMedian - clubLeaguePosition) + league.reputation
                    difference = targetValue - club.reputation
                    club.reputation = rounddp(club.reputation + 0.5 * difference, 0)


        # PROMOTION / RELEGATION LOGIC

        changes = {}

        for league in self.leagues.values():

            clubs = league.getClubs()
            clubList = []

            for club in clubs.values():
                clubList.append(club)

            clubList.sort(key=lambda club: (-club.getSeasonData(league.getLeagueID()).getPoints(), -club.getSeasonData(league.getLeagueID()).getGoalDifference(), -club.getSeasonData(league.getLeagueID()).goalsFor, club.getFullName()))

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
                    changes[club] = (league.getLeagueID(), league.getLeagueAboveID())

            if league.getLeagueBelowID() != 0:
                for club in relegated:
                    changes[club] = (league.getLeagueID(), league.getLeagueBelowID())


        for club, leaguesList in changes.items():
            currentLeagueID, newLeagueID = leaguesList
            club.setLeagueID(newLeagueID)
            self.leagues[currentLeagueID].removeClub(club.getID())
            self.leagues[newLeagueID].addClub(club.getID(), club)

        self.currentSeason += 1

        # CLEARS ALL SEASON DATA FROM PLAYERS AND MOVES SEASON DATA TO HISTORY
        day, month, year = self.dateObject.getDate()

        for player in self.players.values():
            player.seasonHistory[year] = player.seasonData
            player.seasonData = {}


        # CLEARS ALL SEASON DATA FROM CLUBS AND MOVES SEASON DATA TO HISTORY
        for club in self.clubs.values():
            if club.getID() != 0:
                club.seasonHistory[year] = club.seasonData
                club.seasonData = {}


        # FIXTURE ARRANGEMENT

        for league in self.leagues.values():
            league.getFixtures().clear()

        for club in self.clubs.values():
            club.getFixtures().clear()

        for league in self.leagues.values():
            league.updateStartDate(self.dateObject.getDate())
            tempDate = copy.deepcopy(self.dateObject)
            league.arrangeFixtures(tempDate)

            league.seasonCompleted = False
            league.playoffsArranged = False

    def morningDailyUpdate(self):

        day, month, year = self.dateObject.getDate()

        if (day == 15) and (month == 6):
            self.seasonUpdate()

        if (day == 1) and (month == 7):
            self.annualUpdate()

        if self.dateObject.getWeekday() == "Monday":

            # PLAYER DEVELOPMENT
            for player in self.players.values():
                player.development(self)

            for club in self.clubs.values():
                if club.getID() != 0:
                    club.styleFitMultiplier = club.calculateStyleFitMultiplier(self)


        # CHECKS IF ANY TEMPORARY PLAYERS NEED TO BE REMOVED
        players_to_remove = []
        for player in self.players.values():
            if player.isTemporary:
                players_to_remove.append(player)
        for player in players_to_remove:
            del self.players[player.getID()]


        # CHECKS IF SEASONS HAVE FINISHED
        for league in self.leagues.values():
            isCompleted = True
            for fixture in league.fixtures:
                if fixture.isCompleted is False:
                    isCompleted = False
                    break
            league.seasonCompleted = isCompleted

        for league in self.leagues.values():
            if league.seasonCompleted and not league.playoffsArranged:
                tempDate = copy.deepcopy(self.dateObject)
                league.arrangePlayoffs(tempDate, self)
                league.playoffsArranged = True

        # CHECKS FOR UNASSIGNED INJURIES, AND UPDATES CURRENT INJURIES
        for id, player in self.players.items():
            if player.isInjured and player.getInjuryObject() is None:

                clubObject = self.clubs[player.getClubID()]
                fixtures_copy = clubObject.getFixtures().copy()
                fixtures_copy.reverse()
                for fixture in fixtures_copy:
                    if fixture.getScore() is not None:
                        fixture = fixture
                        break

                injuryObject = Injury(player.getID(), fixture)
                player.setInjuryObject(injuryObject)

            elif player.isInjured and player.getInjuryObject() is not None:
                injury = player.getInjuryObject()
                injury.incrementTimeElapsed()
                if injury.getTimeElapsed() == injury.getLength():
                    player.isInjured = False
                    player.condition = 15
                    player.setInjuryObject(None)


        # INCREASES PLAYER CONDITION

        for player in self.players.values():
            player.condition = player.condition + 15
            if player.condition > 100:
                player.condition = 100
            if player.isInjured:
                player.condition = 0

        # CHECKS FOR YOUTH INTAKE
        day, month, year = self.dateObject.getDate()
        if (day == 1) and (month == 4):
            for club in self.clubs.values():
                if club.getID() != 0:
                    youth_intake(self, club)


    def afternoonDailyUpdate(self):
        self.match_checker()
        self.dateObject.advance()


    def match_checker(self):
        dateObject = self.dateObject

        processed = set()

        for club in self.clubs.values():
            for fixture in club.getFixtures():

                if id(fixture) in processed:
                    continue

                if fixture.getDate() == dateObject.getDate():
                    self.match_sim_processing(fixture)

                processed.add(id(fixture))



    def match_sim_processing(self, fixture):

        """
        1 - AI teams select their formation (taken from manager), starting XIs, benches and playing styles (also taken from the manager)
        2 - All players have the league ID and a competition league ID added to their current season league data dictionary
        3 - Clubs have league ID and a competition league ID added to their current season league data dictionary
        4 - Match is simulated using match engine
        5 - Red card flags given during the match are removed so that the player is able to play the next match
        6 - If is a league fixture, the processing is handed over to the league's processing method
        7 - If is a tournament fixture, checks if the scores are level on aggregate and if so, calls extra time. If still level, calls penalties.
        8 - If is a tournament fixture, the processing is handed over to the tournament's processing method.
        9 - Adds goals, assists, clean sheets, appearances etc to player data
        """

        homeTeam, awayTeam = fixture.getTeams()

        tournamentID = fixture.getLeagueID()
        if tournamentID is None:
            tournamentID = fixture.getTournamentID()

        # TEAMS PREPARE TEAMS

        if homeTeam.getID() != self.managers[self.playerManagerID].getClubID() or self.onHoliday:
            formation, hstarting_eleven, hbench, playingStyle = homeTeam.autoPickTeam(self)
            homeTeam.setTeamSheet(formation, hstarting_eleven, hbench, playingStyle)
        else:
            while True:
                team_sheet_menu(homeTeam.getID(), self)
                passed = True
                if homeTeam.formation is None or homeTeam.playing_style is None:
                    passed = False
                else:
                    for player in homeTeam.starting_eleven + homeTeam.bench:
                        if player == None:
                            passed = False
                            break
                if passed:
                    break
                else:
                    print("⚠️ Please ensure your starting XI is complete for the match!")




        if awayTeam.getID() != self.managers[self.playerManagerID].getClubID() or self.onHoliday:
            formation, astarting_eleven, abench, playingStyle = awayTeam.autoPickTeam(self)
            awayTeam.setTeamSheet(formation, astarting_eleven, abench, playingStyle)
        else:
            while True:
                team_sheet_menu(awayTeam.getID(), self)
                passed = True
                if awayTeam.formation is None or awayTeam.playing_style is None:
                    passed = False
                else:
                    for player in awayTeam.starting_eleven + awayTeam.bench:
                        if player == None:
                            passed = False
                            break
                if passed:
                    break
                else:
                    print("⚠️ Please ensure your starting XI is complete for the match!")


        # REGISTERS ALL PLAYERS FOR TOURNAMENT

        for player in homeTeam.starting_eleven + homeTeam.bench:
            if tournamentID not in player.seasonData.keys():
                player.addTournamentToSeasonData(tournamentID, homeTeam.getID())
        for player in awayTeam.starting_eleven + awayTeam.bench:
            if tournamentID not in player.seasonData.keys():
                player.addTournamentToSeasonData(tournamentID, awayTeam.getID())

        # REGISTERS CLUB FOR TOURNAMENT

        if tournamentID not in homeTeam.seasonData.keys():
            homeTeam.addTournamentToSeasonData(tournamentID)
        if tournamentID not in awayTeam.seasonData.keys():
            awayTeam.addTournamentToSeasonData(tournamentID)

        simulate_match(fixture, self)

        # REMOVING RED CARDS
        for player in homeTeam.getPlayers():
            player.isSentOff = False
        for player in awayTeam.getPlayers():
            player.isSentOff = False

        fixture.isCompleted = True

        if fixture.getType() == "league":
            leagueID = fixture.getLeagueID()
            leagueObject = self.leagues[leagueID]
            leagueObject.postMatchProcessing(fixture)


        elif fixture.getType() == "knockout":

            if fixture.getLeg() is None:
                homeScore, awayScore = fixture.getScore()
                if homeScore == awayScore:
                    simulate_match_extra_time(fixture, self)
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
                    simulate_match_extra_time(fixture, self)
                    homeScore, awayScore = fixture.getScore()
                    aggHome = firstLegAwayScore + homeScore  # TeamB's aggregate
                    aggAway = firstLegHomeScore + awayScore  # TeamA's aggregate

                if aggHome == aggAway:
                    simulate_penalties(fixture)

            if fixture.getLeagueID() is not None:
                leagueObject = self.leagues[fixture.getLeagueID()]
                leagueObject.postMatchProcessing(fixture)
            elif fixture.getTournamentID() is not None:
                tournamentObject = self.getTournaments()[fixture.getTournamentID()]
                tournamentObject.postMatchProcessing(fixture)

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

    def getTournaments(self):
        return self.tournaments

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