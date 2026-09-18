

import random
import math
from mathematical_models import poisson_distribution
from mathematical_models import sigmoid
from mathematical_models import random_choices

CARD_PROBABILITY = 0.10
RED_CARD_PROBABILITY = 0.05
AVERAGE_AGGRESSION = 12

MIDFIELD_INFLUENCE = 0.35
SCALING_CONSTANT = 85
HOME_ADVANTAGE = 1.2
CUTOFF_POINT = 40
MAX_ATTRIBUTE_LIMIT = 20
ASSIST_PROBABILITY = 0.85


POSITION_MAPPING = {
        1: "goalkeeper",
        2: "defender",
        3: "defender",
        4: "defender",
        5: "midfielder",
        6: "midfielder",
        7: "midfielder",
        8: "attacker",
        9: "attacker",
        10: "attacker",
    }



def assignMinute(MATCH_TIME_RELATED_CONSTANTS):

    start = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
    end = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"] + MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"]

    minute = random.randint(start, end)
    return minute

def decreaseCondition(teamA, teamB, minute, MATCH_TIME_RELATED_CONSTANTS):

    players = []

    formationA, starting_elevenA, benchA, playingStyleA = teamA.getTeamSheet()
    formationB, starting_elevenB, benchB, playingStyleB = teamB.getTeamSheet()

    for index, player in enumerate(starting_elevenA):
        if player.isSentOff:
            continue
        players.append((player, POSITION_MAPPING[formationA[index]]))

    for index, player in enumerate(starting_elevenB):
        if player.isSentOff:
            continue
        players.append((player, POSITION_MAPPING[formationB[index]]))

    for player, position in players:

        elapsed = minute - MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
        time_factor = 0.8 + 0.4 * (elapsed / MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"])

        if position == "goalkeeper":
            # Goalkeepers lose condition much more slowly
            loss = (0.25 - player.stamina * 0.008)
        else:
            # Outfield players
            loss = (0.95 - player.stamina * 0.02 + player.work_rate * 0.01)

        player.condition = max(0, player.condition - loss * time_factor)

def considerInjuries(team, minute):

    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    injuryChancePerMinutePerTeam = 0.001

    if random.random() < injuryChancePerMinutePerTeam:

        # FILTERS OUT SENT OFF PLAYERS
        players_to_remove = []
        starting_eleven_copy = starting_eleven.copy()
        for player in starting_eleven_copy:
            if player.isSentOff:
                players_to_remove.append(player)
        for player in players_to_remove:
            starting_eleven_copy.remove(player)

        player = random.choice(starting_eleven_copy)
        player.isInjured = True

        event = {
            "minute": minute,
            "team": team,
            "type": "injury",
            "outcome": None,
            "player": player
        }

        return event


def considerSubstitution(team, minute):
    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()

    # RETURNS INSTANTLY IF NOT ENOUGH SUBS OR BENCH IS EMPTY
    if len(bench) == 0:
        return None

    # CHECKS FOR INJURIES - IF SO, PLAYER WILL BE IMMEDIATELY SUBBED
    for indexPosition, player in enumerate(starting_eleven):
        if player.isSentOff:
            continue
        if player.isInjured:
            return player

    starting_eleven_copy = starting_eleven.copy()

    for player in starting_eleven_copy:
        if player.isSentOff:
            starting_eleven_copy.remove(player)

    starting_eleven_copy.sort(key=lambda p: p.condition)


    player = starting_eleven_copy[random.randint(0, len(starting_eleven_copy) - 1)]

    if minute > 50 and player.condition < 40:
        chance = 0.2
        if random.random() < chance:
            return player

    return None



def makeSubstitution(team, player, minute, subCount):

    if subCount <= 0:
        return 0, subCount

    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    for index, playerInList in enumerate(starting_eleven):
        if playerInList == player:
            break

    position = formation[index]

    bench.sort(key=lambda p: p.calculateRating(position) * 0.4 + p.condition * 0.6, reverse=True)
    for candidate in bench:
        if (candidate.calculateRating(position) * candidate.condition > (
                player.calculateRating(position) * player.condition)):
            bench.remove(candidate)
            starting_eleven[index] = candidate

            event = {
                "minute": minute,
                "team": team,
                "type": "substitution",
                "outcome": None,
                "joining-match": candidate,
                "leaving-match": player
            }

            team.setTeamSheet(formation, starting_eleven, bench, playingStyle)
            subCount -= 1
            return event, subCount
        else:
            # FAILED SUBSTITUTION - NO BENEFIT OF MAKING SUB
            return 0, subCount


def calculateFouls(team, MATCH_TIME_RELATED_CONSTANTS):

    playing_style_multipliers = {
        "Possession": 0.85,
        "Tiki Taka": 0.90,
        "Wing Play": 1.00,
        "Gegenpress": 1.30,
        "Counter Attack": 1.10,
        "Route One": 1.20
    }

    teamAggressions = []
    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    for player in starting_eleven:
        if player.isSentOff:
            continue
        teamAggressions.append(player.aggression)
    total = sum(teamAggressions)
    multiplier = (total / len(teamAggressions)) / AVERAGE_AGGRESSION

    teamFoulTotal = MATCH_TIME_RELATED_CONSTANTS["BASE_FOUL_TOTAL"] * multiplier * playing_style_multipliers[playingStyle]

    totalFouls = poisson_distribution(teamFoulTotal)
    return totalFouls


def evaluateFoul(team, minute, events):
    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    candidates = []

    for index in range(len(starting_eleven)):
        if starting_eleven[index].isSentOff:
            continue
        player = starting_eleven[index]
        weight = (player.aggression * 0.40 + (MAX_ATTRIBUTE_LIMIT - player.decision_making) * 0.20 +
                  (MAX_ATTRIBUTE_LIMIT - player.defending) * 0.20 + (MAX_ATTRIBUTE_LIMIT - player.composure) * 0.20)
        candidates.append([player, weight])

    item = random_choices(candidates)
    selectedFouler = item[0]



    if random.random() < CARD_PROBABILITY:
        if random.random() < RED_CARD_PROBABILITY:
            foulType = "red"
        else:
            foulType = "yellow"

            # CHECKS FOR DOUBLE YELLOW
            for event in events:
                if event["type"] == "foul" and event["outcome"] == "yellow" and event["player"] == selectedFouler:
                    foulType = "red"

    else:
        foulType = "no-card"

    event = {
        "minute": minute,
        "team": team,
        "type": "foul",
        "outcome": foulType,
        "player": selectedFouler
    }

    if foulType == "red":
        # REMOVES PLAYER FROM MATCH - SENDING OFF
        for index, player in enumerate(starting_eleven):
            if selectedFouler == player:
                selectedFouler.isSentOff = True

    return event



def calculateChances(clubARatings, clubBRatings, teamObject, homeClub, styleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS):
    formation, starting_eleven, bench, playingStyle = teamObject.getTeamSheet()

    aGoalkeeping, aDefence, aMidfield, aAttack = clubARatings
    bGoalkeeping, bDefence, bMidfield, bAttack = clubBRatings

    threatScore = aAttack - bDefence + ((aMidfield - bMidfield) * MIDFIELD_INFLUENCE)

    if threatScore > CUTOFF_POINT:
        threatScore = CUTOFF_POINT + (threatScore - CUTOFF_POINT) * 0.3

    lmbda = MATCH_TIME_RELATED_CONSTANTS["DEFAULT_CHANCES"] * math.exp(threatScore / SCALING_CONSTANT)

    if homeClub:
        lmbda = lmbda * HOME_ADVANTAGE

    playing_style_multipliers = {
        "Possession": 1.02,
        "Tiki Taka": 1.05,
        "Wing Play": 1.02,
        "Gegenpress": 1.10,
        "Counter Attack": 0.95,
        "Route One": 0.90
    }

    # BOOSTS / DECREASES AMOUNT OF CHANCES DEPENDING ON HOW GOOD A TEAM IS AT PLAYING A PARTICULAR STYLE COMPARED TO THE LEAGUE
    lmbda *= styleFitMultiplier

    chances = poisson_distribution(lmbda * playing_style_multipliers[playingStyle])

    return chances

ROLE_WEIGHT = {"goalkeeper": 0.0, "defender": 0.15, "midfielder": 0.45, "attacker": 1.0}

def evaluateChance(attackingTeam, defendingTeam, minute):

    formation, starting_eleven, bench, playingStyle = attackingTeam.getTeamSheet()
    weights = []

    for index, position in enumerate(formation):
        player = starting_eleven[index]
        if player.isSentOff:
            continue
        group = POSITION_MAPPING[position]
        weights.append([player, ROLE_WEIGHT[group] * player.calculateRating(position)])

    selectedItem = random_choices(weights)
    selectedShooter = selectedItem[0]

    # SELECTS GOALKEEPER FROM DEFENDING SIDE

    dFormation, dStarting_eleven, dBench, dPlayingStyle = defendingTeam.getTeamSheet()
    selectedGoalkeeper = dStarting_eleven[0]


    # CALCULATES SHOT QUALITY BY COMPARING ATTACKER WITH GOALKEEPER
    shotQuality = (selectedShooter.finishing * 0.55 + selectedShooter.composure * 0.15 +
                   selectedShooter.football_iq * 0.15 + selectedShooter.positioning * 0.15 -
                   (selectedGoalkeeper.shot_stopping * 0.60 + selectedGoalkeeper.handling * 0.25 + selectedGoalkeeper.command * 0.15))

    playing_style_multipliers = {
        "Possession": 0.95,
        "Tiki Taka": 1.05,
        "Wing Play": 1.00,
        "Gegenpress": 1.05,
        "Counter Attack": 1.05,
        "Route One": 1.05
    }

    scale = 15 # Dictates how much ratings matter
    goalProbability = sigmoid(shotQuality, scale) * playing_style_multipliers[playingStyle]
    if goalProbability > 0.9:
        goalProbability = 0.9

    if random.random() < goalProbability:
        outcome = "goal"
        formation, starting_eleven, bench, playingStyle = attackingTeam.getTeamSheet()
    else:
        outcome = "miss"
        selectedShooter = None
        selectedAssister = None

    if outcome == "goal":
        # ASSIGNS ASSIST TO GOAL IF NEEDED
        if random.random() < ASSIST_PROBABILITY:
            candidates = []
            for player in starting_eleven:

                if player.isSentOff:
                    continue

                if player == selectedShooter:
                    continue

                weight = player.passing * 0.50 + player.vision * 0.25 + player.decision_making * 0.15 + player.composure * 0.10

                if player == selectedGoalkeeper:
                    weight *= 0.2

                candidates.append([player, weight])

            item = random_choices(candidates)
            selectedAssister = item[0]

        else:
            selectedAssister = None

    event = {
        "minute": minute,
        "team": attackingTeam,
        "type": "chance",
        "outcome": outcome,
        "scorer": selectedShooter,
        "assister": selectedAssister,
        "xG": goalProbability
    }

    return event

def calculateRatings(club):

    positionRatings = [[], [], [], []]
    formation, starting_eleven, bench, playingStyle = club.getTeamSheet()

    for index, position in enumerate(formation):
        rating = starting_eleven[index].calculateRating(position)
        group = POSITION_MAPPING[position]
        if group == "goalkeeper":
            positionRatings[0].append(rating)
        elif group == "defender":
            positionRatings[1].append(rating)
        elif group == "midfielder":
            positionRatings[2].append(rating)
        elif group == "attacker":
            positionRatings[3].append(rating)

    for index, positionRating in enumerate(positionRatings):
        mean = sum(positionRating) / len(positionRating)
        positionRatings[index] = mean

    return positionRatings


def get_match_statistics(fixture, homeTeam, awayTeam, homeRatings, awayRatings):

    formationA, starting_elevenA, benchA, playingStyleA = homeTeam.getTeamSheet()
    formationB, starting_elevenB, benchB, playingStyleB = awayTeam.getTeamSheet()

    events = fixture.getMatchEvents()

    homeBigChances = 0
    awayBigChances = 0
    homeXG = 0
    awayXG = 0
    homeFouls = 0
    awayFouls = 0
    homeYellowCards = 0
    awayYellowCards = 0
    homeRedCards = 0
    awayRedCards = 0

    homeTeam, awayTeam = fixture.getTeams()

    for event in events:

        # Chances / Fouls
        if event["type"] == "chance" and event["team"] == homeTeam:
            homeBigChances += 1
            homeXG += event["xG"]

        elif event["type"] == "chance" and event["team"] == awayTeam:
            awayBigChances += 1
            awayXG += event["xG"]

        elif event["type"] == "foul" and event["team"] == homeTeam:
            homeFouls += 1
            if event["outcome"] == "yellow":
                homeYellowCards += 1
            elif event["outcome"] == "red":
                homeRedCards += 1

        elif event["type"] == "foul" and event["team"] == awayTeam:
            awayFouls += 1
            if event["outcome"] == "yellow":
                awayYellowCards += 1
            elif event["outcome"] == "red":
                awayRedCards += 1

    # SHOTS

    playing_style_multipliers = {
        "Possession": 0.95,
        "Tiki Taka": 0.90,
        "Wing Play": 1.15,
        "Gegenpress": 1.10,
        "Counter Attack": 1.05,
        "Route One": 1.15
    }

    extraShots = poisson_distribution(homeBigChances * 0.5 * playing_style_multipliers[playingStyleA])  # low-quality/speculative efforts beyond the clear-cut chances
    homeShots = homeBigChances + extraShots
    extraShots = poisson_distribution(awayBigChances * 0.5 * playing_style_multipliers[playingStyleB])  # low-quality/speculative efforts beyond the clear-cut chances
    awayShots = awayBigChances + extraShots

    # POSSESSION

    playing_style_multipliers = {
        "Possession": 1.25,
        "Tiki Taka": 1.20,
        "Wing Play": 1.00,
        "Gegenpress": 1.05,
        "Counter Attack": 0.80,
        "Route One": 0.80
    }

    relative_playing_style_multiplier = playing_style_multipliers[playingStyleA] - playing_style_multipliers[playingStyleB] + 1

    aGoalkeeping, aDefence, aMidfield, aAttack = homeRatings
    bGoalkeeping, bDefence, bMidfield, bAttack = awayRatings

    diff = aMidfield - bMidfield
    scale = 70  # controls how sharply midfield dominance swings possession
    homePossession = sigmoid(diff, scale)
    homePossession *= relative_playing_style_multiplier
    homePossession *= 100


    # Add a random swing of +/-5%
    homePossession += random.uniform(-5, 5)
    homePossession = max(0, min(90, round(homePossession)))

    awayPossession = 100 - homePossession

    # PASSES

    playing_style_multipliers = {
        "Possession": 1.15,
        "Tiki Taka": 1.20,
        "Wing Play": 0.95,
        "Gegenpress": 0.90,
        "Counter Attack": 0.75,
        "Route One": 0.65
    }

    basePasses = 100 + homePossession * 6
    homePasses = poisson_distribution(basePasses * playing_style_multipliers[playingStyleA])
    midfieldFactor = 1 + ((homeRatings[2] - awayRatings[2]) / 200)
    homePasses *= midfieldFactor

    basePasses = 100 + awayPossession * 6
    awayPasses = poisson_distribution(basePasses * playing_style_multipliers[playingStyleB])
    midfieldFactor = 1 + ((awayRatings[2] - homeRatings[2]) / 200)
    awayPasses *= midfieldFactor


    matchStatistics = {
        "homePossession": homePossession,
        "awayPossession": awayPossession,
        "homePasses": round(homePasses),
        "awayPasses": round(awayPasses),
        "homeShots": homeShots,
        "awayShots": awayShots,
        "homeBigChances": homeBigChances,
        "awayBigChances": awayBigChances,
        "homeXG": round(homeXG, 2),
        "awayXG": round(awayXG, 2),
        "homeFouls": homeFouls,
        "awayFouls": awayFouls,
        "homeYellowCards": homeYellowCards,
        "awayYellowCards": awayYellowCards,
        "homeRedCards": homeRedCards,
        "awayRedCards": awayRedCards,
    }

    return matchStatistics





def simulate_match(fixture, game):

    """
    1 - The match's "time-related" constants (variables that change depending on the match length) are defined.
    2 - All players who are starting the match have their appearances for the match increased
    3 - Each team's goalkeeping, defending, midfield and attacking ratings are calculated and the style fit multiplier is also fetched from the club objects.
    4 - A team's chances are created by calculating the difference between attack and the opposition defense, and the difference between your midfield and opposition
    midfield, though this is weighted less. This threat score is passed into an exponential, multiplying base chances by the e ** threat score over a scaling constant,
    and this constant can be used to reduce / increase the effect a better team has on their chances created. After the cutoff point, the threat score grows slowly, as
    the amount of chances would grow at an unrealistic rate. This is then passed into a poisson distribution, which can be used to add noise to the static amount of
    chances, as a poisson distribution can be used for modeling independent events.
    5 - The total number of team fouls are calculated by finding the mean of the team's player's aggression attributes. This is divided by an average aggression metric
    to get a multiplier, which is multiplied by the base total fouls pre-determined constant. This is then passed into a poisson distribution, to add noise to the static amount
    of fouls, as a poisson distribution can be used for modeling independent events.
    6 - The total amount of chances and fouls are added to a predeterminedEvents dictionary, where these events are assigned a minute they happen in
    7 - The match loop is run, cycling from the start of the match until the end minute by minute. At the start of every minute, both teams are checked for if they have
    enough players not sent off - if they have 5 players sent off, the team will register a forfeit and the opposing team is awarded a 3-0 win regardless of what has
    happened in the match itself up to that point.
    8 - Player condition is reduced every minute, with a combination of work rate and stamina, along with how deep into the game it is. A team has a 0.001 chance of getting
    an injury to a player per minute, which works out at around a ~10% chance per game.
    9 - Every minute a team will consider making a substitution - if a team has a player injured, it will automatically return that player for immediate substitution. If not,
    it will select a player at random, and if the player has a condition of under 40, and is passed 50 minutes, the player has a 0.2 chance of being subbed off. If being subbed
    off, all players on the bench will be cycled through and giving a score of 0.4 of his ability in the position and 0.6 of his condition. If this surpasses the player being
    subbed off, then the player is subbed off. The 0.2 randomness prevents the manager making objective substitutions as soon as the parameters are met - the manager does not
    know a definitive value of fatigue like is being modeled here.
    10 - If the minute is reached in which a chance happens, the chance is evaluated. A 'shot-quality' score is generated by stats such as the player's finishing, composure,
    football IQ etc, and this is compared with the goalkeepers shot-stopping and diving. This value is passed into a sigmoid, as it perfectly maps this into a probability
    between 0-1, and handles negative values well, with them being assigned a decimal < 0.5. This also acts as the shot XG - as the player's physical position on the pitch
    is abstracted, this takes away the key variable xG is measured on. If there is a goal, there is a 0.85 chance it will be assisted, and all players in the starting XI (
    except the goalkeeper and shot taker) are assigned score of their passing, vision, football IQ, composure, and this is used to select the assister. The chance probability
    is also tweaked slightly by styleFitMultiplier, which considers how suited the team is to playing their style of football, either punishing the manager or benefiting them
    for selecting a style that doesn't match / matches their squad of players.
    11 - If the minute is reached in which a foul happens, each player in the team's starting XI is given a score of their defending, composure, decision-making and aggression,
    where high aggression is punished, and low defending, composure, decision-making are punished. A random player using these weightings is selected, and then is either
    awarded no card, a yellow, or red. If a player receives a red, he is removed from the match. If a player receives a yellow, the game cycles through and checks if they
    have been awarded a yellow previously. If so, the yellow becomes a red, and they are sent off.
    12 - calculateChances, calculateFouls, evaluateChances and evaluateFouls all use weightings to adjust probabilities after the initial values are calculated: for example,
    the possession style / tactic will result in more chances being created but lower conversion rates in evaluateChances, as with a team working the ball around the box,
    they may create many half chances but fewer clear-cut chances. A team who plays counter-attacking football will have fewer chances to break away as they invite pressure,
    but when they do, they often will attack efficiently and with numbers, resulting in a higher conversion rate to reflect a high-quality chance.
    13 - Match statistics are generated, adding up XG (derived from the probability generated from the sigmoid in evaluateChances), all chances, yellow cards, red cards etc.
    Extra shots are generated from half the number of chances and the playing style multiplier. This accounts for speculative efforts that can't be considered a big chance.
    Possession is calculated by finding the difference in midfield and passing it into a sigmoid function - this is because the S shape it generates perfectly mirrors how
    small margins should result in the midfield battle being won or lost, however huge gaps shouldn't result in extreme amounts of possession due to other factors such as
    the other team receiving the ball when it goes out of play and when it is in contention. A multiplier from the team's style of play is then used. Passes is derived from
    possession, and a midfield factor, along with the style fit multiplier. This is passed into a poisson distribution to add some noise / slight variation.
    """


    MATCH_TIME_RELATED_CONSTANTS = {
        "MINUTE_STARTING_FROM": 0,
        "MATCH_LENGTH": 90,
        "BASE_FOUL_TOTAL": 10,
        "DEFAULT_CHANCES": 3
    }

    homeTeam, awayTeam = fixture.getTeams()
    starting_players = []


    formation, starting_eleven, bench, playingStyle = homeTeam.getTeamSheet()
    for player in starting_eleven:
        starting_players.append(player)
    formation, starting_eleven, bench, playingStyle = awayTeam.getTeamSheet()
    for player in starting_eleven:
        starting_players.append(player)

    tournamentID = fixture.getLeagueID()
    if tournamentID is None:
        tournamentID = fixture.getTournamentID()

    for player in starting_players:
        player.seasonData[tournamentID].appearances += 1


    homeRatings = calculateRatings(homeTeam)
    awayRatings = calculateRatings(awayTeam)

    homeStyleFitMultiplier = homeTeam.styleFitMultiplier
    awayStyleFitMultiplier = awayTeam.styleFitMultiplier

    homeChances = calculateChances(homeRatings, awayRatings, homeTeam, True, homeStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)
    awayChances = calculateChances(awayRatings, homeRatings, awayTeam,False, awayStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)

    homeFouls = calculateFouls(homeTeam, MATCH_TIME_RELATED_CONSTANTS)
    awayFouls = calculateFouls(awayTeam, MATCH_TIME_RELATED_CONSTANTS)

    predeterminedEvents = []
    for i in range(homeChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "opposing-team": awayTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(awayChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "opposing-team": homeTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(homeFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    for i in range(awayFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    events = []

    homeSubs = 5
    awaySubs = 5

    homeScore = 0
    awayScore = 0

    start = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
    end = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"] + MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"]

    for minute in range(start, end):

        # CHECKS FOR POSSIBLE FORFEIT IF 5 PLAYERS FROM A TEAM HAVE BEEN SENT OFF
        formation, starting_eleven, bench, playingStyle = homeTeam.getTeamSheet()
        count = 0
        for player in starting_eleven:
            if player.isSentOff:
                count += 1
        if count > 5:
            fixture.matchForfeited = homeTeam
        count = 0
        formation, starting_eleven, bench, playingStyle = awayTeam.getTeamSheet()
        for player in starting_eleven:
            if player.isSentOff:
                count += 1
        if count > 5:
            fixture.matchForfeited = awayTeam

        if fixture.matchForfeited is not False:
            break

        # DECREASING PLAYER CONDITION
        decreaseCondition(homeTeam, awayTeam, minute, MATCH_TIME_RELATED_CONSTANTS)

        # INJURIES

        event = considerInjuries(homeTeam, minute)
        if event is not None:
            events.append(event)

        event = considerInjuries(awayTeam, minute)
        if event is not None:
            events.append(event)


        # CHECKS IF A TEAM WISHES TO MAKE A SUB

        player = considerSubstitution(homeTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(homeTeam, player, minute, homeSubs)
            if event != 0: # FAILED SUBSTITUTION IF NONE IS RETURNED
                events.append(event)
                homeSubs = subCount

        player = considerSubstitution(awayTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(awayTeam, player, minute, awaySubs)
            if event != 0:
                events.append(event)
                awaySubs = subCount

        # EVALUATES EVENTS IF THEY HAPPEN IN THE MINUTE WE'RE IN
        for predeterminedEvent in predeterminedEvents:
            if predeterminedEvent["minute"] == minute:
                if predeterminedEvent["type"] == "chance":
                    event = evaluateChance(predeterminedEvent["team"], predeterminedEvent["opposing-team"], minute)
                    events.append(event)

                    # CHECKS FOR GOAL
                    if event["outcome"] == "goal" and event["team"] == homeTeam:
                        homeScore += 1
                    elif event["outcome"] == "goal" and event["team"] == awayTeam:
                        awayScore += 1

                elif predeterminedEvent["type"] == "foul":
                    event = evaluateFoul(predeterminedEvent["team"], minute, events)
                    events.append(event)

    fixture.setMatchEvents(events)
    statistics = get_match_statistics(fixture, homeTeam, awayTeam, homeRatings, awayRatings)
    fixture.setMatchStatistics(statistics)
    fixture.setScore(homeScore, awayScore)

    if fixture.matchForfeited is not False:
        if fixture.matchForfeited == homeTeam:
            fixture.setScore(0, 3)
        elif fixture.matchForfeited == awayTeam:
            fixture.setScore(3, 0)


def simulate_match_extra_time(fixture, game):

    MATCH_TIME_RELATED_CONSTANTS = {
        "MINUTE_STARTING_FROM": 90,
        "MATCH_LENGTH": 30,
        "BASE_FOUL_TOTAL": 3,
        "DEFAULT_CHANCES": 1
    }


    homeTeam, awayTeam = fixture.getTeams()

    homeRatings = calculateRatings(homeTeam)
    awayRatings = calculateRatings(awayTeam)

    homeStyleFitMultiplier = homeTeam.styleFitMultiplier
    awayStyleFitMultiplier = awayTeam.styleFitMultiplier

    homeChances = calculateChances(homeRatings, awayRatings, homeTeam, True, homeStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)
    awayChances = calculateChances(awayRatings, homeRatings, awayTeam, False, awayStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)

    homeFouls = calculateFouls(homeTeam, MATCH_TIME_RELATED_CONSTANTS)
    awayFouls = calculateFouls(awayTeam, MATCH_TIME_RELATED_CONSTANTS)

    predeterminedEvents = []
    for i in range(homeChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "opposing-team": awayTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(awayChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "opposing-team": homeTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(homeFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    for i in range(awayFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    events = fixture.getMatchEvents()

    homeSubs = 1
    awaySubs = 1

    start = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
    end = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"] + MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"]

    for minute in range(start, end):

        # CHECKS FOR POSSIBLE FORFEIT IF 5 PLAYERS FROM A TEAM HAVE BEEN SENT OFF
        formation, starting_eleven, bench, playingStyle = homeTeam.getTeamSheet()
        count = 0
        for player in starting_eleven:
            if player.isSentOff:
                count += 1
        if count > 5:
            fixture.matchForfeited = homeTeam
        count = 0
        formation, starting_eleven, bench, playingStyle = awayTeam.getTeamSheet()
        for player in starting_eleven:
            if player.isSentOff:
                count += 1
        if count > 5:
            fixture.matchForfeited = awayTeam

        if fixture.matchForfeited is not False:
            break

        # DECREASING PLAYER CONDITION
        decreaseCondition(homeTeam, awayTeam, minute, MATCH_TIME_RELATED_CONSTANTS)

        # INJURIES

        event = considerInjuries(homeTeam, minute)
        if event is not None:
            events.append(event)

        event = considerInjuries(awayTeam, minute)
        if event is not None:
            events.append(event)

        # CHECKS IF A TEAM WISHES TO MAKE A SUB

        player = considerSubstitution(homeTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(homeTeam, player, minute, homeSubs)
            if event != 0:  # FAILED SUBSTITUTION IF 0 IS RETURNED
                events.append(event)
                homeSubs = subCount

        player = considerSubstitution(awayTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(awayTeam, player, minute, awaySubs)
            if event != 0:
                events.append(event)
                awaySubs = subCount

        EThomeScore = 0
        ETawayScore = 0

        # EVALUATES EVENTS IF THEY HAPPEN IN THE MINUTE WE'RE IN
        for predeterminedEvent in predeterminedEvents:
            if predeterminedEvent["minute"] == minute:
                if predeterminedEvent["type"] == "chance":
                    event = evaluateChance(predeterminedEvent["team"], predeterminedEvent["opposing-team"], minute)
                    events.append(event)

                    # CHECKS FOR GOAL
                    if event["outcome"] == "goal" and event["team"] == homeTeam:
                        EThomeScore += 1
                    elif event["outcome"] == "goal" and event["team"] == awayTeam:
                        ETawayScore += 1

                elif predeterminedEvent["type"] == "foul":
                    event = evaluateFoul(predeterminedEvent["team"], minute, events)
                    events.append(event)


    homeScore, awayScore = fixture.getScore()
    fixture.setScore(homeScore + EThomeScore, awayScore + ETawayScore)


    fixture.setMatchEvents(events)
    statistics = get_match_statistics(fixture, homeTeam, awayTeam, homeRatings, awayRatings)
    fixture.setMatchStatistics(statistics)

    if fixture.matchForfeited is not False:
        if fixture.matchForfeited == homeTeam:
            fixture.setScore(0, 3)
        elif fixture.matchForfeited == awayTeam:
            fixture.setScore(3, 0)


def evaluatePenalty(selectedShooter, selectedGoalkeeper):
    # CALCULATES SHOT QUALITY BY COMPARING ATTACKER WITH GOALKEEPER
    shotQuality = (selectedShooter.finishing * 0.55 + selectedShooter.composure * 0.15 +
               selectedShooter.football_iq * 0.15 + selectedShooter.positioning * 0.15 -
                   (selectedGoalkeeper.shot_stopping * 0.60 + selectedGoalkeeper.handling * 0.25 + selectedGoalkeeper.command * 0.15))

    # USES SIGMOID FUNCTION TO CONVERT TO PROBABILITY
    scale = 15  # Dictates how much ratings matter
    goalProbability = sigmoid(shotQuality, scale)

    if random.random() < goalProbability:
        return True
    else:
        return False



def simulate_penalties(fixture):
    homeTeam, awayTeam = fixture.getTeams()

    formationA, starting_elevenA, benchA, playingStyleA = homeTeam.getTeamSheet()
    formationB, starting_elevenB, benchB, playingStyleB = awayTeam.getTeamSheet()

    starting_elevenA_copy = starting_elevenA.copy()
    starting_elevenB_copy = starting_elevenB.copy()

    starting_elevenA_copy.sort(key=lambda p: p.finishing * 0.6 + p.composure * 0.4, reverse=True)
    starting_elevenB_copy.sort(key=lambda p: p.finishing * 0.6 + p.composure * 0.4, reverse=True)

    homeTeamPenaltyTakers = []
    awayTeamPenaltyTakers = []

    events = fixture.getMatchEvents()

    for i in range(len(starting_elevenA_copy)):
        if starting_elevenA_copy[i].isSentOff is True:
            continue
        homeTeamPenaltyTakers.append(starting_elevenA_copy[i])

    for i in range(len(starting_elevenB_copy)):
        if starting_elevenB_copy[i].isSentOff is True:
            continue
        awayTeamPenaltyTakers.append(starting_elevenB_copy[i])

    homeGoalkeeper = starting_elevenA[0]
    awayGoalkeeper = starting_elevenB[0]

    homeScore = 0
    awayScore = 0

    for i in range(5):

        selected_shooter = homeTeamPenaltyTakers[i]
        selected_goalkeeper = awayGoalkeeper

        hasScored = evaluatePenalty(selected_shooter, selected_goalkeeper)
        if hasScored:
            homeScore += 1
            outcome = "scored"
        else:
            outcome = "missed"

        event = {
            "minute": 999,
            "team": homeTeam,
            "type": "penalty",
            "outcome": outcome,
            "taker": selected_shooter,
            "goalkeeper": selected_goalkeeper,
        }

        events.append(event)

        selected_shooter = awayTeamPenaltyTakers[i]
        selected_goalkeeper = homeGoalkeeper

        hasScored = evaluatePenalty(selected_shooter, selected_goalkeeper)
        if hasScored:
            awayScore += 1
            outcome = "scored"
        else:
            outcome = "missed"

        event = {
            "minute": 999,
            "team": awayTeam,
            "type": "penalty",
            "outcome": outcome,
            "taker": selected_shooter,
            "goalkeeper": selected_goalkeeper,
        }

        events.append(event)

        # ENDS SHOOTOUT EARLY IF IMPOSSIBLE TO CATCH UP

        remaining = 5 - (i + 1)

        if homeScore > awayScore + remaining:
            fixture.setPenaltyScore(homeScore, awayScore)
            fixture.setMatchEvents(events)
            return

        if awayScore > homeScore + remaining:
            fixture.setPenaltyScore(homeScore, awayScore)
            fixture.setMatchEvents(events)
            return


    # CHECKS FOR WINNER AFTER FIRST 5

    if homeScore != awayScore:
        fixture.setPenaltyScore(homeScore, awayScore)
        fixture.setMatchEvents(events)
        return

    index = 5

    # SUDDEN DEATH

    while True:

        # Reuse players once everyone has taken one
        if index >= len(homeTeamPenaltyTakers):
            index = 0

        # Home penalty
        homeScored = evaluatePenalty(homeTeamPenaltyTakers[index], awayGoalkeeper)

        events.append({
            "minute": 999,
            "team": homeTeam,
            "type": "penalty",
            "outcome": "scored" if homeScored else "missed",
            "taker": homeTeamPenaltyTakers[index],
            "goalkeeper": awayGoalkeeper,
        })

        if homeScored:
            homeScore += 1

        # Away penalty
        awayScored = evaluatePenalty(awayTeamPenaltyTakers[index], homeGoalkeeper)

        events.append({
            "minute": 999,
            "team": awayTeam,
            "type": "penalty",
            "outcome": "scored" if awayScored else "missed",
            "taker": awayTeamPenaltyTakers[index],
            "goalkeeper": homeGoalkeeper,
        })

        if awayScored:
            awayScore += 1

        # Sudden death
        if homeScored != awayScored:
            fixture.setPenaltyScore(homeScore, awayScore)
            fixture.setMatchEvents(events)
            return

        index += 1




