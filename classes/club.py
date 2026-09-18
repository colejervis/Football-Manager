from registry import get_class
import math

from mathematical_models import softmax, random_choices
from player_generation_engine import generate_player

ClubSeasonData = get_class("ClubSeasonData")

class Club:
    FORMATIONS = {
        433: [1, 2, 3, 3, 4, 5, 6, 6, 8, 10, 9],
        4231: [1, 2, 3, 3, 4, 5, 5, 8, 7, 9, 10],
        442: [1, 2, 3, 3, 4, 8, 6, 6, 9, 10, 10],
        5221: [1, 2, 3, 3, 3, 4, 5, 5, 7, 7, 10],
        5212: [1, 2, 3, 3, 3, 4, 5, 5, 7, 10, 10],
        532: [1, 2, 3, 3, 3, 4, 5, 6, 6, 10, 10],
        352: [1, 3, 3, 3, 5, 8, 6, 6, 9, 10, 10],
    }

    PLAYING_STYLES = ["Tiki Taka", "Possession", "Wing Play", "Gegenpress", "Route One", "Counter Attack"]

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

    def __init__(self, club_id, full_name, short_name, nickname, founded_date, transfer_budget, primary_color, secondary_color, reputation, league_id):
        self.id = int(club_id)
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
        self.leagueID = int(league_id)
        self.managerID = 0
        self.stadiumID = 0

        self.squadSelection = {
            "formation": None,
            "playing_style": None,
            "formation_position_mapping": {},
            "bench": None
        }

        self.formation = None
        self.playing_style = None
        self.starting_eleven = []
        self.bench = []

        self.StyleFitMultiplier = 1

        self.seasonHistory = {}
        self.seasonData = {}

    def getLeagueID(self):
        return self.leagueID

    def setLeagueID(self, leagueID):
        self.leagueID = int(leagueID)

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

    def getPlayers(self):
        return self.players

    def addPlayer(self, player):
        self.players.append(player)

    def getFirstTeam(self):
        return self.first_team

    def getYouthTeam(self):
        return self.youth_team

    def setManagerID(self, managerID):
        self.managerID = managerID

    def getManagerID(self):
        return self.managerID

    def setStadiumID(self, stadiumID):
        self.stadiumID = stadiumID

    def getStadiumID(self):
        return self.stadiumID

    def printColors(self):
        return f"{self.COLOR_MAPPING[self.primary_color]}{self.COLOR_MAPPING[self.secondary_color]}"

    def addFixture(self, fixture):
        self.fixtures.append(fixture)

    def getFixtures(self):
        return self.fixtures

    def autoPickTeam(self, game, type="match"):

        """
        1 - Gets formation and playing style from the manager
        2 - Filters through injured players and removes them from the pool of available players
        3 - If there is not enough players for the starting XI and bench in the pool of available players, temporary ones are generated - these are removed
        immediately after the match
        4 - Arranges positions from least populated to most; ensures versatile players are picked for positions where depth is scarce
        5 - Starting XI selection is split into two types - match, where the team will rotate, or a deterministic best XI used in the media prediction menu
        6 - If match is selected, each player who can play in the position is assigned a score. These scores are passed into a softmax function and chosen
        randomly, generating squad rotation. If no players can play the position, the best suited player will play out of position there
        7 - If Best XI is selected, every player who can play the position is considered and given a score (ability in the position), the player with the best
        score takes the position. If there are no players who can play the position, the best suited player will play out of position there.
        8 - The bench is populated, and will try to add a goalkeeper, center-back, center-mid and striker. It will populate the rest of the bench with the
        highest rated non-selected players.
        """

        starting_eleven = []
        bench = []
        MAX_SIZE_OF_BENCH = 7

        managers = game.getManagers()
        manager = managers[self.managerID]

        # GETS PREFERRED FORMATION FROM MANAGER

        if self.formation is None:
            formation = Club.FORMATIONS[manager.getPreferredFormation()]
        else:
            formation = self.formation

        # GETS PREFERRED PLAYING STYLE FROM MANAGER
        if self.playing_style is None:
            playing_style = manager.getPreferredPlayingStyle()
        else:
            playing_style = self.playing_style


        # Filters through injured players and remove them
        available_players = self.first_team.copy()
        players_to_remove = []
        for player in available_players:
            if player.isInjured:
                players_to_remove.append(player)
        for player in players_to_remove:
            available_players.remove(player)

        # IF NOT ENOUGH AVAILABLE PLAYERS, GENERATE TEMPORARY NEW ONES
        if len(available_players) < 11 + MAX_SIZE_OF_BENCH:
            players_to_generate = (11 + MAX_SIZE_OF_BENCH) - len(available_players)
            for i in range(players_to_generate):
                player = generate_player(game, self, "temporary")
                available_players.append(player)
                game.getPlayers()[player.getID()] = player

        # ARRANGES POSITIONS FROM LEAST POPULATED TO MOST
        position_playerCount = []
        for position in formation:
            count = 0
            for player in available_players:
                if player.canPlayPosition(position):
                    count += 1
            position_playerCount.append((position, count))

        new_position_order = []
        while len(position_playerCount) != 0:
            least_tuple = None
            least_count = 999
            for item in position_playerCount:
                position, count = item
                if count < least_count:
                    least_tuple = item
                    least_count = count
            new_position_order.append(least_tuple[0])
            position_playerCount.remove(least_tuple)

        position_player = []
        if type == "match":
            for position in new_position_order:
                candidates = []
                scores = []
                for player in available_players:
                    if player.canPlayPosition(position):
                        score = player.calculateRating(position) * (player.condition / 100)
                        candidates.append(player)
                        scores.append(score)

                if len(candidates) != 0:

                # IF CANDIDATES ISN'T EMPTY
                    weights = []
                    for player in candidates:
                        score = player.calculateRating(position) * (player.condition / 100)
                        weights.append(score)

                    weights = softmax(weights, 15)

                    candidate_weights = []
                    for index, candidate in enumerate(candidates):
                        candidate_weights.append([candidate, weights[index]])

                    item = random_choices(candidate_weights)
                    chosen = item[0]

                    position_player.append((position, chosen))
                    available_players.remove(chosen)

                else:

                # IF CANDIDATES IS EMPTY

                    player_suitability = {}
                    for player in available_players:
                        score = player.calculateRating(position) * player.condition
                        player_suitability[player] = score

                    best_player = None
                    for player, score in player_suitability.items():
                        if best_player is None:
                            best_player = player
                        else:
                            if player_suitability[player] > player_suitability[best_player]:
                                best_player = player

                    position_player.append((position, best_player))
                    available_players.remove(best_player)



        elif type == "bestXI":


            for position in new_position_order:

                player_suitability = {}
                for player in available_players:
                    score = player.calculateRating(position)
                    player_suitability[player] = score

                best_player = None
                for player in available_players:
                    if player.canPlayPosition(position):
                        # CHECKS IF THERE IS NO CURRENTLY SELECTED BEST PLAYER
                        if best_player is None:
                            best_player = player
                        else:
                            if player_suitability[player] > player_suitability[best_player]:
                                best_player = player
                    else:
                        continue

                # TAKES BEST SUITED PLAYER IF NO PLAYER CAN PLAY THE POSITION
                if best_player is None:
                    for player, score in player_suitability.items():
                        if best_player is None:
                            best_player = player
                        else:
                            if player_suitability[player] > player_suitability[best_player]:
                                best_player = player



                position_player.append((position, best_player))

                # REMOVES SELECTED PLAYER FROM AVAILABLE PLAYERS
                available_players.remove(best_player)

        # PUTS THEM BACK INTO FORMATION ORDER
        for position in formation:
            for index, item in enumerate(position_player):
                intended_position, player = item

                if intended_position == position:
                    starting_eleven.append(player)
                    position_player.pop(index)
                    break


        available_players.sort(key=lambda p: p.calculateRating(), reverse=True)

        # ENSURES BENCH HAS A GOALKEEPER, DEFENDER, MIDFIELDER, WINGER AND STRIKER

        position_added = {
            1: False,
            3: False,
            6: False,
            10: False,
        }

        players_to_remove = []
        for player in available_players:
            if player.getPositionID() == 1 and position_added[1] == False:
                position_added[1] = True
                bench.append(player)
                players_to_remove.append(player)
            elif player.getPositionID() == 3 and position_added[3] == False:
                position_added[3] = True
                bench.append(player)
                players_to_remove.append(player)
            elif player.getPositionID() == 6 and position_added[6] == False:
                position_added[6] = True
                bench.append(player)
                players_to_remove.append(player)
            elif player.getPositionID() == 10 and position_added[10] == False:
                position_added[10] = True
                bench.append(player)
                players_to_remove.append(player)

        for players in players_to_remove:
            available_players.remove(players)

        # ORGANIZES REMAINING PLAYERS BASED ON ABILITY TO GET BENCH

        for i in range(MAX_SIZE_OF_BENCH - len(bench)):
            bench.append(available_players[i])

        return formation, starting_eleven, bench, playing_style

    def calculateTeamStrength(self, game):

        """
        This IS NOT USED in the match engine - only calculateBettingOdds
        """

        formation, starting_eleven, bench, playing_style = Club.autoPickTeam(self, game, "bestXI")
        starting_eleven_total = 0
        bench_total = 0
        for index, player in enumerate(starting_eleven):
            position = formation[index]
            starting_eleven_total = (player.calculateRating(position)) + starting_eleven_total
        for index, player in enumerate(bench):
            bench_total = (player.calculateRating()) + bench_total

        starting_eleven_mean = starting_eleven_total / len(starting_eleven)
        bench_mean = bench_total / len(bench)

        # STARTING XI HAS MORE IMPORTANCE - ALL PLAYERS HAVE IMPACT IN XI THEREFORE USES TOTAL, NOT ALL PLAYERS ON BENCH WILL BE USED HENCE MEAN
        score = (starting_eleven_mean * 0.95) + (bench_mean * 0.05)
        return round(score)


    def calculateBettingOdds(self, game):

        """
        Softmax function - raises e to the power of the value returned in calculateTeamStrength() and divides it by the temperature

        1 - This score (from calculateTeamStrength() and the club's reputation) is divided by the total to get a probability
        2 - This is converted to fractional odds form by finding the reciprocal of the probability and subtracting 1
        """

        leagues = game.getLeagues()
        leagueObject = leagues[self.leagueID]
        clubsInLeague = leagueObject.getClubs()
        clubs = game.getClubs()

        temperature = 6

        scores = []

        for club in clubsInLeague:
            clubObject = clubs[club]
            strength = clubObject.calculateTeamStrength(game) * 0.8 + clubObject.reputation * 0.2
            scores.append(math.exp(strength / temperature))

        total = sum(scores)

        my_score = math.exp((self.calculateTeamStrength(game) * 0.8 + self.reputation * 0.2) / temperature)

        probability = my_score / total

        decimal_odds = 1 / probability
        fractional = decimal_odds - 1


        # ONLY ROUNDS LONG ODDS
        if fractional >= 100:
            fractional = round(fractional / 50) * 50
        elif fractional >= 20:
            fractional = round(fractional / 10) * 10
        else:
            fractional = round(fractional)

        return int(fractional)


    def calculateStyleFitMultiplier(self, game):

        """
        Used in match engine, but calculated by the club's own object every week for performance reasons. This considers how well a team's
        squad is suited to a play style, and compares it with the league average.

        1 - For every club in the club's league, for every outfield player at the club, their attributes are multiplied by the weightings below for
        their club's playing style, and the mean score of all players at the club is compared with the league average.

        2 - The strength of this is weakened slightly by a strength variable, with a number in the range of -1 to 1 being multiplied by the strength
        and then has 1 added back to it to act as a standard multiplier.
        """

        STYLE_FIT_PROFILES = {
            "Possession": {"passing": 0.30, "ball_control": 0.25, "vision": 0.20, "composure": 0.15,
                           "decision_making": 0.10},
            "Tiki Taka": {"passing": 0.35, "vision": 0.25, "ball_control": 0.25, "decision_making": 0.15},
            "Wing Play": {"delivery": 0.30, "pace": 0.25, "dribbling": 0.20, "ball_control": 0.15,
                          "decision_making": 0.10},
            "Gegenpress": {"work_rate": 0.25, "stamina": 0.20, "aggression": 0.15, "pace": 0.15, "defending": 0.15,
                           "decision_making": 0.10},
            "Counter Attack": {"pace": 0.30, "decision_making": 0.20, "vision": 0.20, "finishing": 0.15,
                               "composure": 0.15},
            "Route One": {"aerial": 0.35, "strength": 0.25, "pace": 0.25, "composure": 0.15},
        }

        leagues = game.getLeagues()
        leagueObject = leagues[self.getLeagueID()]
        clubs = leagueObject.getClubs()

        club_styleFitScore = {}

        for club in clubs.values():
            formation, starting_eleven, bench, playingStyle = club.getTeamSheet()

            # IF TEAM SHEET NOT SET YET, IT WILL GET PLAYING STYLE FROM MANAGER INSTEAD
            if playingStyle is None:
                managers = game.getManagers()
                playingStyle = managers[club.managerID].getPreferredPlayingStyle()

            players_to_assess = []
            clubPlayers = club.getPlayers()
            clubPlayers.sort(key=lambda p: p.calculateRating(), reverse=True)
            for player in clubPlayers[:15]:
                if player.getPositionID() != 1:
                    players_to_assess.append(player)
            totalScore = 0
            for player in players_to_assess:
                playerScore = 0
                for attribute, weight in STYLE_FIT_PROFILES[playingStyle].items():
                    playerScore += getattr(player, attribute) * weight
                totalScore += playerScore
            averageScore = totalScore / len(players_to_assess)
            club_styleFitScore[club] = averageScore

        running_total = 0
        for club, score in club_styleFitScore.items():
            if club != self:
                running_total += score

        leagueAvg = running_total / (len(club_styleFitScore) - 1)
        teamAvg = club_styleFitScore[self]

        ratio = teamAvg / leagueAvg

        strength = 0.5  # 0 = no effect, 1 = full effect
        return 1 + (ratio - 1) * strength

    def autoSplitPlayers(self, game):

        """
        Splits players into first team and youth team .

        1 - All players are given a first team suitability score, using 80% of their current ability and 20% of their potential, which is than multiplied
        by an age multiplier, to make older players more slightly more likely than players under 21 to be part of the first team.
        2 - Iterates through all positions and tries to add in the specified amount of players in the target depth matrix. It will add all players who's first
        position is that position to a candidates list and sorts it by their suitability score. It will iterate through the desired number of players or the
        number of suitable candidates, and adds them to the first team.
        3 - It loops over all positions again, checking if there are enough players who can play the position. If not, it will add players who can somewhat
        play the position.
        4 - It adds all remaining players to the youth team
        5 - It checks if there are any remaining outliers by comparing the 3rd worst first team player (not 1st or 2nd as those players may be worse than the
        rest of the squad) to the best 5 youth players. If any of the youth players are better, they are promoted.
        """

        date = game.getDateObject()

        self.first_team = []
        self.youth_team = []

        players_firstTeamSuitabilityScore = {}

        age_factor_mapping = [
            [1, 0.75],
            [15, 0.80],
            [16, 0.85],
            [17, 0.90],
            [18, 0.94],
            [19, 0.97],
            [20, 0.99],
            [21, 1.00],
        ]

        for player in self.players:

            age_multiplier = 0

            for tier in age_factor_mapping:
                ageRequired = tier[0]
                ageMultiplier = tier[1]

                if ageRequired > player.getAge(date):
                    break
                else:
                    age_multiplier = ageMultiplier

            abilityScore = (player.calculateRating() * 0.8) + (player.potential * 0.2)
            firstTeamSuitabilityScore = abilityScore * age_multiplier

            players_firstTeamSuitabilityScore[player] = firstTeamSuitabilityScore

        SQUAD_DEPTH_CURRENT_DEPTH = {
            1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
        }

        SQUAD_DEPTH_TARGET_DEPTH = {
            1: 2, 2: 2, 3: 3, 4: 2, 5: 2, 6: 3, 7: 2, 8: 2, 9: 2, 10: 2,
        }

        playersCopy = self.players.copy()

        # FIRST PASS FOR PRIMARY POSITIONS

        for position, targetDepth in SQUAD_DEPTH_TARGET_DEPTH.items():

            candidates = []
            playersToRemove = []

            for player in playersCopy:
                if player.getPositionID() == position:
                    candidates.append(player)
            candidates.sort(key=lambda player: players_firstTeamSuitabilityScore[player], reverse=True)

            if len(candidates) < targetDepth:
                targetDepth = len(candidates)

            for i in range(targetDepth):
                SQUAD_DEPTH_CURRENT_DEPTH[position] += 1
                self.first_team.append(candidates[i])
                playersToRemove.append(candidates[i])

            for player in playersToRemove:
                playersCopy.remove(player)


        newOrder = []
        for position, positionDepth in SQUAD_DEPTH_TARGET_DEPTH.items():
            tuple = position, positionDepth
            newOrder.append(tuple)

        newOrder.sort(key=lambda tuple: tuple[1])

        # SECOND PASS FOR SECONDARY POSITIONS TO ENSURE SUFFICIENT DEPTH

        positions = game.getPositions()
        for tuple in newOrder:

            position, positionDepth = tuple
            targetDepth = SQUAD_DEPTH_TARGET_DEPTH[position]

            count = SQUAD_DEPTH_CURRENT_DEPTH[position]

            if count < targetDepth:

                candidates = []
                playersToRemove = []

                for player in playersCopy:
                    if player.canPlayPosition(positions[position]):
                        candidates.append(player)
                candidates.sort(key=lambda player: players_firstTeamSuitabilityScore[player], reverse=True)

                slotsNeeded = targetDepth - count

                if len(candidates) < slotsNeeded:
                    slotsNeeded = len(candidates)

                for i in range(slotsNeeded):
                    self.first_team.append(candidates[i])
                    playersToRemove.append(candidates[i])

                for player in playersToRemove:
                    playersCopy.remove(player)

        # ADD REMAINING PLAYERS TO YOUTH / RESERVE SQUAD

        for player in playersCopy:
            self.youth_team.append(player)


        if len(self.first_team) >= 3 and len(self.youth_team) >= 6:
            # CHECKS IF THERE ARE ANY OUTLIERS IN RESERVE SQUAD

            players_to_promote = []
            first_team_copy = self.first_team.copy()
            youth_team_copy = self.youth_team.copy()
            first_team_copy.sort(key = lambda player: player.calculateRating())
            youth_team_copy.sort(key=lambda player: player.calculateRating(), reverse=True)
            player_for_comparison = first_team_copy[2]

            for i in range(5):
                    if youth_team_copy[i].calculateRating() > player_for_comparison.calculateRating():
                        players_to_promote.append(youth_team_copy[i])

            for player in players_to_promote:
                self.first_team.append(player)
                self.youth_team.remove(player)


    def addTournamentToSeasonData(self, tournamentID):
        self.seasonData[tournamentID] = ClubSeasonData()

    def getTeamSheet(self):
        return self.formation, self.starting_eleven, self.bench, self.playing_style

    def setTeamSheet(self, formation, starting_eleven, bench, playing_style):
        self.formation = formation
        self.starting_eleven = starting_eleven
        self.bench = bench
        self.playing_style = playing_style

    def getSeasonData(self, tournamentID, year="current"):

        if year == "current":
            seasonData = self.seasonData
        else:
            seasonData = self.seasonHistory[year]

        if tournamentID not in seasonData:
            self.addTournamentToSeasonData(tournamentID)
        return seasonData[tournamentID]