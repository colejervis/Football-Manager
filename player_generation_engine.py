import random
import math
import random

from mathematical_models import bell_curve, softmax, rounddp, roundsf, random_choices

from classes.player import Player

BASE_POTENTIAL = 160
POTENTIAL_STANDARD_DEV = 30

def generate_random_position():

    # GENERATING POSITION

    position_weights = [
        [1, 0.05],
        [2, 0.09],
        [3, 0.15],
        [4, 0.09],
        [5, 0.10],
        [6, 0.16],
        [7, 0.10],
        [8, 0.09],
        [9, 0.09],
        [10, 0.08],
    ]

    item = random_choices(position_weights)
    selectedPosition = item[0]

    return selectedPosition

def get_random_attributes(selectedPosition):
    YOUTH_GK_PROFILE = {
        "passing": 6, "dribbling": 3, "finishing": 1, "defending": 2, "ball_control": 4, "delivery": 4, "vision": 5,
        "football_iq": 3, "positioning": 4, "composure": 6, "decision_making": 6,
        "work_rate": 5, "aggression": 2, "pace": 5, "strength": 6, "aerial": 6, "stamina": 4, "shot_stopping": 8,
        "handling": 7, "distribution": 6, "command": 5,
    }

    YOUTH_CB_PROFILE = {
        "passing": 7, "dribbling": 4, "finishing": 2, "defending": 9, "ball_control": 5, "delivery": 4,
        "vision": 5,
        "football_iq": 2, "positioning": 9, "composure": 6, "decision_making": 7,
        "work_rate": 7, "aggression": 6, "pace": 7, "strength": 7, "aerial": 8, "stamina": 7,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    YOUTH_FULLBACK_PROFILE = {
        "passing": 7, "dribbling": 7, "finishing": 3, "defending": 7, "ball_control": 7, "delivery": 6, "vision": 6,
        "football_iq": 4, "positioning": 7, "composure": 6, "decision_making": 6,
        "work_rate": 8, "aggression": 6, "pace": 8, "strength": 6, "aerial": 5, "stamina": 8,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    YOUTH_CDM_PROFILE = {
        "passing": 8, "dribbling": 5, "finishing": 3, "defending": 7, "ball_control": 7, "delivery": 4, "vision": 7,
        "football_iq": 6, "positioning": 8, "composure": 7, "decision_making": 7,
        "work_rate": 8, "aggression": 6, "pace": 6, "strength": 7, "aerial": 5, "stamina": 8,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    YOUTH_CM_PROFILE = {
        "passing": 8, "dribbling": 7, "finishing": 4, "defending": 6, "ball_control": 8, "delivery": 5,
        "vision": 8,
        "football_iq": 8, "positioning": 4, "composure": 7, "decision_making": 7,
        "work_rate": 8, "aggression": 4, "pace": 6, "strength": 5, "aerial": 4, "stamina": 8,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    YOUTH_CAM_PROFILE = {
        "passing": 8, "dribbling": 8, "finishing": 6, "defending": 2, "ball_control": 8, "delivery": 7,
        "vision": 9,
        "football_iq": 8, "positioning": 2, "composure": 7, "decision_making": 7,
        "work_rate": 5, "aggression": 3, "pace": 7, "strength": 4, "aerial": 2, "stamina": 6,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    YOUTH_WINGER_PROFILE = {
        "passing": 7, "dribbling": 8, "finishing": 5, "defending": 2, "ball_control": 8, "delivery": 7,
        "vision": 7,
        "football_iq": 7, "positioning": 2, "composure": 6, "decision_making": 6,
        "work_rate": 6, "aggression": 3, "pace": 9, "strength": 4, "aerial": 2, "stamina": 7,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    YOUTH_ST_PROFILE = {
        "passing": 5, "dribbling": 7, "finishing": 8, "defending": 1, "ball_control": 8, "delivery": 3,
        "vision": 5,
        "football_iq": 9, "positioning": 1, "composure": 7, "decision_making": 6,
        "work_rate": 6, "aggression": 5, "pace": 8, "strength": 7, "aerial": 6, "stamina": 6,
        "shot_stopping": 1, "handling": 1, "distribution": 1, "command": 1,
    }

    position_attribute_mapping = {
        1: YOUTH_GK_PROFILE,
        2: YOUTH_FULLBACK_PROFILE,
        3: YOUTH_CB_PROFILE,
        4: YOUTH_FULLBACK_PROFILE,
        5: YOUTH_CDM_PROFILE,
        6: YOUTH_CM_PROFILE,
        7: YOUTH_CAM_PROFILE,
        8: YOUTH_WINGER_PROFILE,
        9: YOUTH_WINGER_PROFILE,
        10: YOUTH_ST_PROFILE,
    }

    profile = position_attribute_mapping[selectedPosition].copy()

    attributes = {}

    for attribute, base_score in profile.items():
        score = bell_curve(base_score, 1)
        score = max(1, min(20, score))
        attributes[attribute] = score

    return attributes

def generate_random_nationality(game, club, databaseType):

    """
    1 - https://en.wikipedia.org/wiki/Logistic_function
    Sigmoid Logistic function - Acts similarly to a normal sigmoid function (converts raw data to a decimal value between 0 and 1, useful as a probability)
    but a logistic function allows me to change the midpoint and horizontal stretch - the functions below were calibrated in Desmos to closely match the waypoints of:

    Fake (Generated Database):
    (100, ~0.85), (160, ~0.4) - Lower reputation clubs have less international spots available and less attraction to foreign players - higher rep clubs get
    better value for money buying from abroad

    Youth Intakes:
    (100, ~0.95), (160, ~0.85): High reputation clubs have the reach to take in international youngsters, but is still dominated by home nation players

    2 - If it is a foreign player, a list of foreign nations and their equivalent reputations are generated
    3 - If the home nation has 'neighboring nations' assigned, these nations receive a reputation boost before softmax which uses the same home nation probabilities from before
    4 - The reputations are passed into a softmax function to amplify the probability differences between high caliber footballing nations and low caliber nations
    """
    if databaseType == "fake":
        homeNationProbabilty = 1/(1+math.exp(0.041 * (club.reputation-140)))
    elif databaseType == "youth":
        homeNationProbabilty = 1 / (1 + math.exp(0.02 * (club.reputation - 250)))


    home_nation_id = game.getLeagues()[club.getLeagueID()].getNationID()
    nations = game.getNations()

    if random.random() < homeNationProbabilty:
        return nations[home_nation_id]

    foreign_nations = []
    for nation_id, nation in nations.items():
        if nation_id != home_nation_id:
            foreign_nations.append(nation)

    reputations = []
    for nation in foreign_nations:
        reputations.append(nation.getReputation())

    neighbouring_nations = {
        1: [2, 3, 4, 5]
    }
    neighbouring_nations_boost = 60 * homeNationProbabilty
    if home_nation_id in neighbouring_nations:
        neighbouring_nations_list = neighbouring_nations[home_nation_id]
        for index, item in enumerate(foreign_nations):
            if item.getID() in neighbouring_nations_list:
                reputations[index] += neighbouring_nations_boost


    weights = softmax(reputations, 7)

    weight_list = []
    for index, weight in enumerate(weights):
        weight_list.append([foreign_nations[index], weight])

    item = random_choices(weight_list)
    nation = item[0]
    return nation



def generate_random_name(game, selectedNationality):
    firstLastNameLists = game.names[selectedNationality.getID()]

    firstNames = firstLastNameLists[0]
    surNames = firstLastNameLists[1]

    firstname = firstNames[random.randint(0, len(firstNames) - 1)]
    surname = surNames[random.randint(0, len(surNames) - 1)]

    return firstname, surname


def generate_random_potential(game, club, new_player):
    clubReputation = club.reputation

    league = game.getLeagues()[club.leagueID]
    leagueReputation = league.getReputation()
    nationReputation = game.getNations()[league.getNationID()].getReputation()

    reputation = ((clubReputation * 0.4) + (nationReputation * 0.3) + (leagueReputation * 0.3))
    reputation_multiplier = (reputation / 200)

    potential = bell_curve(BASE_POTENTIAL * reputation_multiplier, POTENTIAL_STANDARD_DEV)

    # Clamps values
    potential = min(200, max(potential,0))

    return int(rounddp(potential, 0))

def generate_random_age():
    age = bell_curve(26, 3.5)
    age = round(max(17, min(age, 34)))
    return age

def generate_wage(game, player):
    """
    1 - Generates a wage based on player ability
    2 - Generates a modifier from 0-1 to reduce player wages for youngsters, who are likely on entry-level youth contracts or scholarships
    16: ~0.4, 17: ~0.48, 18: ~0.55, 19: ~0.64, 20: ~0.74, 21: ~0.86
    3 - Adds some noise / variance by putting it through the bell curve
    """

    ca = player.calculateRating()
    age = player.getAge(game.getDateObject())
    wage = 6.102885 * math.exp(0.061161 * ca)

    if age < 22:

        wage *= math.exp(0.15 * (age - 22))

    wage = bell_curve(wage, 1.2)

    return int(roundsf(wage, 2))

def generate_player(game, club, type, ID=None, position=None):

    if type == "youth":
        contractLength = random.randint(3, 4)
        age = random.randint(16, 17)
        wage = roundsf(random.randint(350, 500), 2)
    elif type == "temporary":
        contractLength = 1
        age = generate_random_age()
        wage = 0

    if position is None:
        selectedPosition = generate_random_position()
    else:
        selectedPosition = position


    # SELECTING ATTRIBUTES
    attributes = get_random_attributes(selectedPosition)

    # NATIONALITY
    selectedNationality = generate_random_nationality(game, club, "youth")

    # NAME
    firstname, surname = generate_random_name(game, selectedNationality)

    # GENERATES PLAYER
    if ID is None:
        new_player_id = max(game.getPlayers().keys()) + 1
    else:
        new_player_id = ID

    # Birthday
    current_day, current_month, current_year = game.getDateObject().getDate()
    birth_year = current_year - age
    birth_month = random.randint(1, 12)
    days_in_month = game.getDateObject().daysInMonth[birth_month - 1]
    birth_day = random.randint(1, days_in_month)

    new_player = Player(
        new_player_id,
        firstname,
        surname,
        birth_day,
        birth_month,
        birth_year,
        selectedNationality.getID(),
        club.id,
        selectedPosition,
        attributes["passing"],
        attributes["dribbling"],
        attributes["finishing"],
        attributes["defending"],
        attributes["ball_control"],
        attributes["delivery"],
        attributes["vision"],
        attributes["football_iq"],
        attributes["positioning"],
        attributes["composure"],
        attributes["decision_making"],
        attributes["work_rate"],
        attributes["aggression"],
        attributes["pace"],
        attributes["strength"],
        attributes["stamina"],
        attributes["aerial"],
        attributes["shot_stopping"],
        attributes["handling"],
        attributes["distribution"],
        attributes["command"],
        1,
        random.randint(165, 195),
        wage,
        contractLength,
    )

    if type == "temporary":
        new_player.isTemporary = True


    # POTENTIAL
    potential = generate_random_potential(game, club, new_player)
    new_player.potential = potential

    return new_player


def generate_fake_player(game, club, ID=None, position=None):

    if position is None:
        selectedPosition = generate_random_position()
    else:
        selectedPosition = position


    # SELECTING ATTRIBUTES
    attributes = get_random_attributes(selectedPosition)

    # NATIONALITY
    selectedNationality = generate_random_nationality(game, club, "fake")

    # NAME
    firstname, surname = generate_random_name(game, selectedNationality)

    # GENERATES PLAYER
    if ID is None:
        new_player_id = max(game.getPlayers().keys()) + 1
    else:
        new_player_id = ID

    # Birthday
    age = generate_random_age()

    current_day, current_month, current_year = game.getDateObject().getDate()
    birth_year = current_year - age
    birth_month = random.randint(1, 12)
    days_in_month = game.getDateObject().daysInMonth[birth_month - 1]
    birth_day = random.randint(1, days_in_month)

    new_player = Player(
        new_player_id,
        firstname,
        surname,
        birth_day,
        birth_month,
        birth_year,
        selectedNationality.getID(),
        club.id,
        selectedPosition,
        attributes["passing"],
        attributes["dribbling"],
        attributes["finishing"],
        attributes["defending"],
        attributes["ball_control"],
        attributes["delivery"],
        attributes["vision"],
        attributes["football_iq"],
        attributes["positioning"],
        attributes["composure"],
        attributes["decision_making"],
        attributes["work_rate"],
        attributes["aggression"],
        attributes["pace"],
        attributes["strength"],
        attributes["stamina"],
        attributes["aerial"],
        attributes["shot_stopping"],
        attributes["handling"],
        attributes["distribution"],
        attributes["command"],
        1,
        random.randint(165, 195),
        0,
        random.randint(1, 4),
    )


    return new_player



def player_ability_bell_curve(player_count, mean, standard_deviation):
    """
    Runs the gaussian distribution for each player, clamps ratings between 1 and 200, and rounds the ability
    """

    raw_ratings = []
    for i in range(player_count):
        raw_ratings.append(bell_curve(mean, standard_deviation))

    bounded_and_rounded = []
    for i in raw_ratings:
        bounded_and_rounded.append(round(max(1.0, min(i, 200.0))))

    bounded_and_rounded.sort(reverse=True)
    return bounded_and_rounded



def build_fake_player_database(game):

    """
    1 - Cycles through positions assigning an amount of players (depth) between 1-4. CBs and CMs are more common as they typically have at least
    two players in starting XI.

    2 - Assigns mean starting eleven rating as 90% of club rep and reserves as 80% of club rep.

    3 - Passes those means into a bell curve to generate player ratings for starting XI and reserves, where players are naturally centered around the mean
    with occasional outliers at either side

    4 - FISHER-YATES shuffle algorithm - iterating through squad_depth_by_position means that defensive positions are more likely to
    take up the higher ratings in predetermined_abilities - this resulted in defensive players being higher rated than attackers.
    All positions for each player are added into a single list and iterated through.

    5 - Iterates through the positions in the list, generating a player for each. It will find the range of indexes in the ability list, find the
    maximum index, and apply a modifier based on their age and pass that into a bell curve with slight standard deviation. This helps create a slight
    correlation with ability and age, where players in their peak will be higher rated than players in the latter stages of their career or youngsters.
    The ability at the index that is returned from the bell curve will be applied to the player.

    6 -  Potential ability is generated for the player (which also uses a bell curve with a base mean, with reputation applied). To prevent players having
    a lower potential than ability, a clamp is used where if this is the case, potential is set as ability + 5.

    7 - The player attribute increase development algorithm is run until the player reaches their assigned ability.

    8 - Generates a ten player youth academy.
    """


    for club in game.getClubs().values():

        if club.getID() == 0:
            continue
        else:
            players = club_generate_fake_players(game, club)
            for player in players:
                game.players[player.getID()] = player


def club_generate_fake_players(game, club):

    id_count = len(game.getPlayers()) + 1
    players = []

    squad_depth_by_position = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    for position, depth in squad_depth_by_position.items():

        if position == 3 or position == 6:
            position_depth_probability = [
                [2, 0.1],
                [3, 0.3],
                [4, 0.4],
                [5, 0.2],
            ]
        else:
            position_depth_probability = [
                [1, 0.2],
                [2, 0.3],
                [3, 0.3],
                [4, 0.2],
            ]

        item = random_choices(position_depth_probability)
        depth = item[0]

        squad_depth_by_position[position] = depth


    rep = club.reputation + random.randint(-3, 3)
    starting_eleven_mean = rep * 0.90
    reserves_mean = rep * 0.80

    total_squad_size = sum(squad_depth_by_position.values())
    starting_eleven_approx_abilities = player_ability_bell_curve(11, starting_eleven_mean, random.randint(6, 7))
    reserves_approx_abilities = player_ability_bell_curve(total_squad_size - 11, reserves_mean, random.randint(7, 8))

    predetermined_abilities = starting_eleven_approx_abilities + reserves_approx_abilities
    predetermined_abilities.sort()

    positions = []
    for position, depth in squad_depth_by_position.items():
        for i in range(depth):
            positions.append(position)

    i = len(positions) - 1
    while i > 0:
        j = random.randint(0, i)
        positions[i], positions[j] = positions[j], positions[i]
        i -= 1

    for position in positions:

        player = generate_fake_player(game, club, id_count, position)

        age = player.getAge(game.getDateObject())

        if age <= 21:
            modifier = random.uniform(0.30, 0.65)
        elif age <= 26:
            modifier = random.uniform(0.75, 0.95)
        elif age <= 31:
            modifier = random.uniform(0.85, 1.00)
        else:
            modifier = random.uniform(0.60, 0.90)

        target_index = round((len(predetermined_abilities) - 1) * modifier)

        index = round(bell_curve(target_index, 1.5))
        index = max(0, min(index, len(predetermined_abilities) - 1))

        ability = predetermined_abilities[index]
        predetermined_abilities.remove(ability)

        potential = generate_random_potential(game, club, player)
        player.potential = max(potential, ability + 5)

        while ability > player.calculateRating():
            player.development_attribute_increase()

        player.current_wage = generate_wage(game, player)

        players.append(player)

        id_count += 1

    return players



def youth_intake(game, club):

    YOUTH_INTAKE_SIZE = random.randint(8, 10)

    clubReputation = club.reputation

    league = game.getLeagues()[club.leagueID]
    leagueReputation = league.getReputation()
    nationReputation = game.getNations()[league.getNationID()].getReputation()

    reputation = (clubReputation * 0.4) + (nationReputation * 0.3) + (leagueReputation * 0.3)

    reserves_approx_abilities = player_ability_bell_curve(YOUTH_INTAKE_SIZE, reputation * 0.65, 2)

    # Doing max(game.players.keys() for every player generation is expensive, a running total improves performance)
    next_available_ID = max(game.getPlayers().keys()) + 1

    for i in range(YOUTH_INTAKE_SIZE):
        player = generate_player(game, club, "youth", next_available_ID)

        index = random.randint(0, len(reserves_approx_abilities) - 1)
        pre_determined_ability = reserves_approx_abilities[index]
        reserves_approx_abilities.remove(pre_determined_ability)

        while player.calculateRating() < pre_determined_ability:
            player.development_attribute_increase()

        player.potential = max(player.potential, player.calculateRating() + 5)

        # ADDS PLAYER TO GAME
        game.getPlayers()[player.getID()] = player
        # Add player to club roster
        if game.currentSeason != game.startingSeason:
            club.players.append(player)

        next_available_ID += 1

    # RE-EVALUATES YOUTH AND FIRST TEAM SQUAD
    club.autoSplitPlayers(game)






