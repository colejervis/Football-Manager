
import random
from registry import get_class
import math
from mathematical_models import rounddp, random_choices

PlayerSeasonData = get_class("PlayerSeasonData")

class Player:
    GOALKEEPER_WEIGHTINGS = [
        ["passing", 0.01],
        ["dribbling", 0.00],
        ["finishing", 0.00],
        ["defending", 0.01],
        ["ball_control", 0.01],
        ["delivery", 0.00],
        ["vision", 0.01],
        ["football_iq", 0.02],
        ["positioning", 0.02],
        ["composure", 0.04],
        ["decision_making", 0.06],
        ["work_rate", 0.01],
        ["aggression", 0.01],
        ["pace", 0.02],
        ["strength", 0.02],
        ["aerial", 0.00],
        ["stamina", 0.00],
        ["shot_stopping", 0.32],
        ["handling", 0.20],
        ["distribution", 0.12],
        ["command", 0.12],
    ]

    GOALKEEPER_WEIGHTINGS_DICT = {}
    for item in GOALKEEPER_WEIGHTINGS:
        GOALKEEPER_WEIGHTINGS_DICT[item[0]] = item[1]

    CENTREBACK_WEIGHTINGS = [
        ["passing", 0.03],
        ["dribbling", 0.01],
        ["finishing", 0.01],
        ["defending", 0.18],
        ["ball_control", 0.03],
        ["delivery", 0.01],
        ["vision", 0.02],
        ["football_iq", 0.00],
        ["positioning", 0.15],
        ["composure", 0.06],
        ["decision_making", 0.06],
        ["work_rate", 0.03],
        ["aggression", 0.06],
        ["pace", 0.07],
        ["strength", 0.12],
        ["aerial", 0.14],
        ["stamina", 0.02],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    CENTREBACK_WEIGHTINGS_DICT = {}
    for item in CENTREBACK_WEIGHTINGS:
        CENTREBACK_WEIGHTINGS_DICT[item[0]] = item[1]

    FULLBACK_WEIGHTINGS = [
        ["passing", 0.08],
        ["dribbling", 0.07],
        ["finishing", 0.01],
        ["defending", 0.16],
        ["ball_control", 0.05],
        ["delivery", 0.10],
        ["vision", 0.04],
        ["football_iq", 0.05],
        ["positioning", 0.09],
        ["composure", 0.04],
        ["decision_making", 0.05],
        ["work_rate", 0.07],
        ["aggression", 0.02],
        ["pace", 0.09],
        ["strength", 0.03],
        ["aerial", 0.02],
        ["stamina", 0.03],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    FULLBACK_WEIGHTINGS_DICT = {}
    for item in FULLBACK_WEIGHTINGS:
        FULLBACK_WEIGHTINGS_DICT[item[0]] = item[1]

    DEFENSIVE_MIDFIELDER_WEIGHTINGS = [
        ["passing", 0.09],
        ["dribbling", 0.02],
        ["finishing", 0.02],
        ["defending", 0.13],
        ["ball_control", 0.05],
        ["delivery", 0.02],
        ["vision", 0.05],
        ["football_iq", 0.07],
        ["positioning", 0.08],
        ["composure", 0.06],
        ["decision_making", 0.08],
        ["work_rate", 0.08],
        ["aggression", 0.05],
        ["pace", 0.04],
        ["strength", 0.05],
        ["aerial", 0.05],
        ["stamina", 0.06],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    DEFENSIVE_MIDFIELDER_WEIGHTINGS_DICT = {}
    for item in DEFENSIVE_MIDFIELDER_WEIGHTINGS:
        DEFENSIVE_MIDFIELDER_WEIGHTINGS_DICT[item[0]] = item[1]

    CENTRAL_MIDFIELDER_WEIGHTINGS = [
        ["passing", 0.12],
        ["dribbling", 0.06],
        ["finishing", 0.02],
        ["defending", 0.05],
        ["ball_control", 0.10],
        ["delivery", 0.02],
        ["vision", 0.10],
        ["football_iq", 0.09],
        ["positioning", 0.04],
        ["composure", 0.05],
        ["decision_making", 0.10],
        ["work_rate", 0.10],
        ["aggression", 0.02],
        ["pace", 0.04],
        ["strength", 0.03],
        ["aerial", 0.01],
        ["stamina", 0.05],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    CENTRAL_MIDFIELDER_WEIGHTINGS_DICT = {}
    for item in CENTRAL_MIDFIELDER_WEIGHTINGS:
        CENTRAL_MIDFIELDER_WEIGHTINGS_DICT[item[0]] = item[1]

    ATTACKING_MIDFIELDER_WEIGHTINGS = [
        ["passing", 0.11],
        ["dribbling", 0.10],
        ["finishing", 0.06],
        ["defending", 0.01],
        ["ball_control", 0.10],
        ["delivery", 0.04],
        ["vision", 0.13],
        ["football_iq", 0.09],
        ["positioning", 0.01],
        ["composure", 0.10],
        ["decision_making", 0.11],
        ["work_rate", 0.04],
        ["aggression", 0.01],
        ["pace", 0.05],
        ["strength", 0.01],
        ["aerial", 0.01],
        ["stamina", 0.02],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    ATTACKING_MIDFIELDER_WEIGHTINGS_DICT = {}
    for item in ATTACKING_MIDFIELDER_WEIGHTINGS:
        ATTACKING_MIDFIELDER_WEIGHTINGS_DICT[item[0]] = item[1]

    WINGER_WEIGHTINGS = [
        ["passing", 0.06],
        ["dribbling", 0.16],
        ["finishing", 0.08],
        ["defending", 0.01],
        ["ball_control", 0.10],
        ["delivery", 0.10],
        ["vision", 0.05],
        ["football_iq", 0.07],
        ["positioning", 0.01],
        ["composure", 0.04],
        ["decision_making", 0.06],
        ["work_rate", 0.04],
        ["aggression", 0.01],
        ["pace", 0.17],
        ["strength", 0.01],
        ["aerial", 0.01],
        ["stamina", 0.02],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    WINGER_WEIGHTINGS_DICT = {}
    for item in WINGER_WEIGHTINGS:
        WINGER_WEIGHTINGS_DICT[item[0]] = item[1]

    STRIKER_WEIGHTINGS = [
        ["passing", 0.01],
        ["dribbling", 0.05],
        ["finishing", 0.15],
        ["defending", 0.01],
        ["ball_control", 0.05],
        ["delivery", 0.01],
        ["vision", 0.01],
        ["football_iq", 0.12],
        ["positioning", 0.03],
        ["composure", 0.12],
        ["decision_making", 0.07],
        ["work_rate", 0.03],
        ["aggression", 0.03],
        ["pace", 0.10],
        ["strength", 0.09],
        ["aerial", 0.10],
        ["stamina", 0.02],
        ["shot_stopping", 0],
        ["handling", 0],
        ["distribution", 0],
        ["command", 0],
    ]

    STRIKER_WEIGHTINGS_DICT = {}
    for item in STRIKER_WEIGHTINGS:
        STRIKER_WEIGHTINGS_DICT[item[0]] = item[1]

    SECONDARY_POSITION_FAMILIARITY = 0.95
    UNKNOWN_POSITION_FAMILIARITY = 0.8

    secondary_position_mapping = {
        1: [],
        2: [8],
        4: [9],
        3: [2, 4],
        6: [5, 7],
        5: [6],
        7: [6],
        9: [8, 4],
        8: [9, 2],
        10: [],
    }

    def __init__(self, player_id, firstname, surname, birthDay, birthMonth, birthYear, nationID, clubID, positionID,
                 passing, dribbling, finishing, defending, ball_control, delivery,
                 vision, football_iq, positioning, composure, decision_making, work_rate, aggression,
                 pace, strength, stamina, aerial, shot_stopping, handling, distribution, command,
                 potential, height, current_wage, contract_length):
        self.id = int(player_id)
        self.firstname = firstname
        self.surname = surname
        self.birthDay = int(birthDay)
        self.birthMonth = int(birthMonth)
        self.birthYear = int(birthYear)
        self.nationID = int(nationID)
        self.clubID = int(clubID)
        self.parentClubID = int(clubID)
        self.loanClubID = None
        self.positionID = int(positionID)
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

        self.isTemporary = False

        self.development_bank = 0

        self.isSentOff = False
        self.condition = 100
        self.isInjured = False
        self.injuryObject = None

        self.seasonHistory = {}
        self.seasonData = {}


    def calculateMarketValue(self, game):

        """
        1 - Determines multipliers for factors involving age (high impact), contract length (high impact), club, league
        and league nation reputation.
        2 - Piecewise exponential modeling used to map player rating to a base transfer value, using the following benchmarks:
        190 (Best player in world): 200M, 140 (Decent Premier League Player / Top Championship): 30M, 105 (Decent League One / High League Two): 900K
        90 (Decent League Two / High National League): 200K, 80 (Decent National League, High NL North/South): 60K, 70 (Decent NL North/South): 5K
        """

        clubs = game.getClubs()
        leagues = game.getLeagues()
        nations = game.getNations()

        # SETS MARKET VALUE TO 0 IF PLAYER IS FREE AGENT
        if self.clubID == 0:
            return 0

        DateObject = game.getDateObject()
        age = self.getAge(DateObject)

        age_factor_mapping = [
            [1, 1.2],
            [21, 1.1],
            [25, 1.05],
            [28, 1.0],
            [31, 0.9],
            [33, 0.8],
            [35, 0.7],
            [37, 0.6],
            [40, 0.5],
        ]

        age_multiplier = 0
        for tier in age_factor_mapping:
            ageRequired = tier[0]
            multiplier = tier[1]

            if ageRequired > age:
                break
            else:
                age_multiplier = multiplier

        club_reputation_mapping = [
            [1, 0.7],
            [75, 0.8],
            [90, 0.9],
            [105, 1.0],
            [112, 1.0],
            [120, 1.1],
            [140, 1.2],
        ]

        clubObject = clubs[self.clubID]
        clubReputation = clubObject.getReputation()

        club_reputation_multiplier = 0
        for tier in club_reputation_mapping:
            reputationRequired = tier[0]
            multiplier = tier[1]

            if reputationRequired > clubReputation:
                break
            else:
                club_reputation_multiplier = multiplier

        league_reputation_mapping = [
            [1, 0.90],
            [99, 0.95],
            [129, 0.1],
            [142, 0.1],
            [154, 1.05],
        ]

        leagueID = clubObject.getLeagueID()
        leagueObject = leagues[leagueID]
        leagueReputation = leagueObject.getReputation()

        league_reputation_multiplier = 0
        for tier in league_reputation_mapping:
            reputationRequired = tier[0]
            multiplier = tier[1]

            if reputationRequired > leagueReputation:
                break
            else:
                league_reputation_multiplier = multiplier

        league_nation_reputation_mapping = [
            [1, 0.9],
            [111, 1.0],
            [119, 1.0],
            [127, 1.0],
            [136, 1.0],
            [154, 1.05],
            [175, 1.1],
        ]

        nationID = leagueObject.getNationID()
        nationObject = nations[nationID]
        nationReputation = nationObject.getReputation()

        nation_reputation_multiplier = 0
        for tier in league_nation_reputation_mapping:
            reputationRequired = tier[0]
            multiplier = tier[1]

            if reputationRequired > nationReputation:
                break
            else:
                nation_reputation_multiplier = multiplier

        contract_length_mapping = [
            [1, 0.6],
            [2, 0.8],
            [3, 1.0],
            [4, 1.0],
            [5, 1.1],
            [6, 1.1],
        ]

        contract_length_multiplier = 0
        for tier in contract_length_mapping:
            contractLengthRequired = tier[0]
            multiplier = tier[1]

            if contractLengthRequired > self.contract_length:
                break
            else:
                contract_length_multiplier = multiplier

        multiplier = (
                league_reputation_multiplier
                * age_multiplier
                * nation_reputation_multiplier
                * club_reputation_multiplier
                * contract_length_multiplier
        )


        # USING EXPONENTIAL MODELLING

        if Player.calculateRating(self) < 70:
            value = 0 # Players of this ability are most likely semi-professional
        elif Player.calculateRating(self) < 80:
            value = 0.00013954 * (1.28209 ** Player.calculateRating(self)) # Non-professional players to
        elif Player.calculateRating(self) < 90:
            value = 3.9491 * (1.1279 ** Player.calculateRating(self)) # Mid-tier League Two players to top end League Two
        elif Player.calculateRating(self) < 105:
            value = 24.029 * (1.1055 ** Player.calculateRating(self)) # Mid-tier League Two to top end League Two
        elif Player.calculateRating(self) < 140:
            value = 24.249 * (1.1054 ** Player.calculateRating(self)) # League One to decent Premier League
        elif Player.calculateRating(self) < 190:
            value = 147199 * (1.0387 ** Player.calculateRating(self)) # Premier League + Elite Players
        else:
            value = 250000000 # MAX VALUE - No team will pay more than this on one player

        value = value * multiplier
        value = float(f"{value:.2g}")
        value = int(value)

        return value

    # ENSURES KEY ATTRIBUTES GROW RAPIDLY
    def high_curve(x):
        return (x / 10) ** 1.25 * 10

    # ENSURES DECENTLY IMPORTANT ATTRIBUTES GROW EXPONENTIALLY
    def mid_curve(x):
        return (x / 10) ** 1.1 * 10


    def calculateRating(self, position=None):


        if position is None:
            position = self.positionID

        position_weights = {
            1: self.GOALKEEPER_WEIGHTINGS_DICT,
            3: self.CENTREBACK_WEIGHTINGS_DICT,
            2: self.FULLBACK_WEIGHTINGS_DICT,
            4: self.FULLBACK_WEIGHTINGS_DICT,
            5: self.DEFENSIVE_MIDFIELDER_WEIGHTINGS_DICT,
            6: self.CENTRAL_MIDFIELDER_WEIGHTINGS_DICT,
            7: self.ATTACKING_MIDFIELDER_WEIGHTINGS_DICT,
            9: self.WINGER_WEIGHTINGS_DICT,
            8: self.WINGER_WEIGHTINGS_DICT,
            10: self.STRIKER_WEIGHTINGS_DICT
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

        if position != self.positionID and self.canPlayPosition(position):
            ability = ability * Player.SECONDARY_POSITION_FAMILIARITY
        elif position != self.positionID and not self.canPlayPosition(position):
            ability = ability * Player.UNKNOWN_POSITION_FAMILIARITY

        return int(round(ability))


    def canPlayPosition(self, position):
        primary = self.positionID
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

    def getNationID(self):
        return self.nationID

    def setPositionID(self, positionID):
        self.positionID = positionID

    def getPositionID(self):
        return self.positionID

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

    def getClubID(self):
        return self.clubID

    def getParentClubID(self):
        return self.parentClubID

    def getLoanClubID(self):
        return self.loanClubID

    def setClubID(self, clubID):
        if clubID is not None:
            self.clubID = int(clubID)
        else:
            self.clubID = None

    def setParentClubID(self, parentClubID):
        if parentClubID is not None:
            self.parentClubID = int(parentClubID)
        else:
            self.parentClubID = None

    def setLoanClubID(self, loanID):
        if loanID is not None:
            self.loanClubID = int(loanID)
        else:
            self.loanClubID = None

    def getInjuryObject(self):
        return self.injuryObject

    def setInjuryObject(self, injuryObject):
        self.injuryObject = injuryObject

    def calculateStarRating(self, players, position = None):

        """
        1 - Normalizes the data type into a dictionary to avoid any type errors
        2 - Calculates mean of players in the list
        3 - Uses sigmoid function to calculate star rating - perfectly mirrors how small changes around the mean can create fine margins and players at the extremes
        are rated as such
        4 - Rounds star rating to nearest 0.5 and maps it onto star rating emojis
        """

        if position is None:
            position = self.positionID

        star_emojis = {
            0.0: "⚪⚪⚪⚪⚪",
            0.5: "🟡⚫⚫⚫⚫",
            1.0: "🟢⚫⚫⚫⚫",
            1.5: "🟢🟡⚫⚫⚫",
            2.0: "🟢🟢⚫⚫⚫",
            2.5: "🟢🟢🟡⚫⚫",
            3.0: "🟢🟢🟢⚫⚫",
            3.5: "🟢🟢🟢🟡⚫",
            4.0: "🟢🟢🟢🟢⚫",
            4.5: "🟢🟢🟢🟢🟡",
            5.0: "🟢🟢🟢🟢🟢"
        }

        if not players:
            return "🟢🟢🟢⚫⚫"


        if type(players) == list:
            tempDict = {}
            for player in players:
                tempDict[player.getID()] = player
            players = tempDict

        total_rating = 0
        for player in players.values():
            total_rating += player.calculateRating()
        mean = total_rating / len(players)

        stars = 5 / (1 + math.exp(-0.065 * (self.calculateRating(position) - mean)))

        stars = rounddp(stars * 2, 0) / 2

        returnValue = star_emojis[stars]

        return returnValue

    def addTournamentToSeasonData(self, tournamentID, clubID = None):
        if clubID is None:
            clubID = self.clubID
        self.seasonData[tournamentID] = PlayerSeasonData(clubID)


    def calculatePlayingPercentage(self, clubs):
        if self.clubID == 0:
            return 0

        total_appearances = 0
        for tournament in self.seasonData.values():
            total_appearances += tournament.appearances

        clubObject = clubs[self.clubID]
        club_matches = 0
        for tournament in clubObject.seasonData.values():
            club_matches += tournament.matchesPlayed

        if club_matches == 0:
            return 0

        return (total_appearances / club_matches) * 100

    def development(self, game):

        if self.calculateRating() >= self.potential:
            return

        clubs = game.getClubs()
        date = game.getDateObject()

        age_points_mapping = [
            [1, 0.19],
            [19, 0.12],
            [21, 0.05],
            [25, 0.03],
            [28, 0.015],
            [30, 0.008],
            [32, -0.07],
            [33, -0.14],
            [34, -0.21],
            [35, -0.28],
        ]

        for tier in age_points_mapping:
            ageRequired = tier[0]
            points = tier[1]

            if ageRequired > self.getAge(date):
                break
            else:
                additional_points = points

        playing_percentage_mapping = [
            [1, 0.5],
            [30, 0.7],
            [50, 1],
            [60, 1.05],
            [70, 1.1],
            [80, 1.2],
            [90, 1.3],
        ]

        playing_percentage_multiplier = 1

        for tier in playing_percentage_mapping:
            percentageRequired = tier[0]
            multiplier = tier[1]

            if percentageRequired > self.calculatePlayingPercentage(clubs):
                break
            else:
                playing_percentage_multiplier = multiplier

        club_reputation_mapping = [
            [1, 0.9],
            [75, 1],
            [90, 1.05],
            [110, 1.1],
            [120, 1.2],
            [140, 1.3],
        ]

        clubObject = clubs[self.clubID]
        clubReputation = clubObject.getReputation()

        club_reputation_multiplier = 1

        for tier in club_reputation_mapping:
            reputationRequired = tier[0]
            multiplier = tier[1]

            if reputationRequired > clubReputation:
                break
            else:
                club_reputation_multiplier = multiplier


        position_weights = {
            1: self.GOALKEEPER_WEIGHTINGS,
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

        if additional_points > 0:
            multiplier = club_reputation_multiplier * playing_percentage_multiplier
            additional_points *= multiplier
        elif additional_points < 0:
            playing_percentage_multiplier = 2 - playing_percentage_multiplier
            multiplier = playing_percentage_multiplier
            additional_points *= multiplier

        self.development_bank += additional_points

        if self.development_bank >= 1:
            self.development_attribute_increase()
            self.development_bank -= 1

        elif self.development_bank <= -1:
            self.development_attribute_decrease()
            self.development_bank += 1


    def development_attribute_increase(self):

        position_weights = {
            1: self.GOALKEEPER_WEIGHTINGS,
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

        weights = position_weights[self.positionID]

        RANDOMNESS = 0.60
        randomised_weights = []
        for attribute, weight in weights:
            if weight == 0:
                randomised_weight = 0
            else:
                random_factor = random.uniform(1 - RANDOMNESS, 1 + RANDOMNESS)
                randomised_weight = weight * random_factor
            randomised_weights.append([attribute, randomised_weight])

        if not randomised_weights:
            return

        items_to_remove = []
        for item in randomised_weights:
            attributeName = item[0]
            if getattr(self, attributeName) >= 20:
                items_to_remove.append(item)
        for item in items_to_remove:
            randomised_weights.remove(item)

        '''
        The formula: modifier = 1 - math.exp(-k * abs(attributeValue - 20))
        Will produce a value between 1 and 0 with k changing how steep it declines
        from 1 to 0 closer to 20
        
        Used to slow down development in attributes which are already closing in on being maxxed out
        
        Lower values for k mean it tails toward 0 at lower attributes - More well rounded players
        '''

        for index, item in enumerate(randomised_weights):
            attributeName = item[0]
            weight = item[1]
            attributeValue = getattr(self, attributeName)
            k = 0.05
            modifier = 1 - math.exp(-k * abs(attributeValue - 20))

            weight *= modifier
            randomised_weights[index] = [attributeName, weight]


        total = 0
        for item in randomised_weights:
            randomised_weight = item[1]
            total += randomised_weight
        for index, item in enumerate(randomised_weights):
            attributeName = item[0]
            randomised_weight = item[1]
            randomised_weights[index] = [attributeName, (randomised_weight / total)]

        item = random_choices(randomised_weights)
        attributeName = item[0]

        current = getattr(self, attributeName)
        setattr(self, attributeName, current + 1)



    def development_attribute_decrease(self):
        DECLINE_OUTFIELD_WEIGHTINGS = [
            ["passing", 0.04],
            ["dribbling", 0.06],
            ["finishing", 0.04],
            ["defending", 0.01],
            ["ball_control", 0.05],
            ["delivery", 0.03],
            ["vision", 0.03],
            ["football_iq", 0.06],
            ["positioning", 0.04],
            ["composure", 0.03],
            ["decision_making", 0.05],
            ["work_rate", 0.03],
            ["aggression", 0.02],
            ["pace", 0.24],
            ["strength", 0.09],
            ["aerial", 0.03],
            ["stamina", 0.15],
        ]

        DECLINE_GOALKEEPER_WEIGHTINGS = [
            ["passing", 0.03],
            ["dribbling", 0.02],
            ["finishing", 0.01],
            ["defending", 0.01],
            ["ball_control", 0.03],
            ["delivery", 0.02],
            ["vision", 0.03],
            ["football_iq", 0.15],
            ["positioning", 0.07],
            ["composure", 0.12],
            ["decision_making", 0.09],
            ["work_rate", 0.02],
            ["aggression", 0.02],
            ["pace", 0.13],
            ["strength", 0.07],
            ["aerial", 0.08],
            ["stamina", 0.02],
            ["shot_stopping", 0.03],
            ["handling", 0.03],
            ["distribution", 0.03],
            ["command", 0.03],
        ]

        if self.positionID == 1:
            weights = DECLINE_GOALKEEPER_WEIGHTINGS
            goalkeeper_decline_probability = 0.5

            if random.uniform(0, 1) < goalkeeper_decline_probability:
                return
        else:
            weights = DECLINE_OUTFIELD_WEIGHTINGS

        item = random_choices(weights)
        attributeName = item[0]

        if getattr(self, attributeName) > 1:
            current = getattr(self, attributeName)
            setattr(self, attributeName, current - 1)




    def getSeasonData(self, tournamentID, year="current"):

        if year == "current":
            seasonData = self.seasonData
        else:
            seasonData = self.seasonHistory[year]

        if tournamentID not in seasonData:
            self.addTournamentToSeasonData(tournamentID)
        return seasonData[tournamentID]

